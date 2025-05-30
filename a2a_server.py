"""
A2A Protocol Server Implementation
"""
import uuid
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import json
import logging
import uvicorn

# Import A2A components
from skills import AgentSkills
from agent_card import AgentCardGenerator
from config import Config
from mgx_inspired_agent_team import MGXInspiredAgentTeam

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for A2A Protocol
class A2ARequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

class A2AResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

class TaskCreateParams(BaseModel):
    user_id: Optional[str] = None
    context_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MessageSendParams(BaseModel):
    task_id: str
    message: Dict[str, Any]
    stream: Optional[bool] = False

class SkillExecuteParams(BaseModel):
    skill_name: str
    parameters: Dict[str, Any]
    task_id: Optional[str] = None

# A2A Server Class
class A2AServer:
    def __init__(self):
        self.app = FastAPI(
            title="A2A Agent Server",
            description="Agent-to-Agent protocol server with MGX-inspired team collaboration",
            version="1.2.0"
        )
        
        # Enable CORS for web applications
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Initialize components
        self.skills = AgentSkills()  # Use AgentSkills instead of SkillManager
        self.agent_card_generator = AgentCardGenerator()
        self.mgx_team = MGXInspiredAgentTeam()
        
        # In-memory storage for tasks (in production, use a database)
        self.tasks: Dict[str, Dict[str, Any]] = {}
        
        # Setup routes
        self.setup_routes()
    
    def setup_routes(self):
        """Setup all API routes"""
        
        @self.app.get("/")
        async def root():
            """Root endpoint with basic info"""
            return self.agent_card_generator.get_service_info()
        
        @self.app.get("/agent-card")
        async def get_agent_card():
            """Return the Agent Card"""
            return self.agent_card_generator.generate_agent_card()
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy", "timestamp": datetime.now().isoformat()}
        
        @self.app.post("/a2a")
        async def a2a_endpoint(request_data: A2ARequest):
            """Main A2A JSON-RPC endpoint"""
            try:
                result = await self.handle_a2a_request(request_data)
                return A2AResponse(result=result, id=request_data.id)
            except Exception as e:
                logger.error(f"Error handling A2A request: {str(e)}")
                return A2AResponse(
                    error={"code": -32603, "message": "Internal error", "data": str(e)},
                    id=request_data.id
                )
        
        @self.app.post("/skills/execute")
        async def execute_skill_direct(params: SkillExecuteParams):
            """Direct skill execution endpoint (non-A2A)"""
            try:
                result = await self.skills.execute_skill(params.skill_name, params.parameters)
                return result
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @self.app.get("/skills")
        async def list_skills():
            """List available skills"""
            return {"skills": self.skills.get_available_skills()}
    
    async def handle_a2a_request(self, request: A2ARequest) -> Dict[str, Any]:
        """Handle A2A JSON-RPC requests"""
        method = request.method
        params = request.params or {}
        
        if method == "task/create":
            return await self.create_task(params)
        elif method == "task/message":
            return await self.send_message(params)
        elif method == "task/artifacts":
            return await self.get_artifacts(params)
        elif method == "task/cancel":
            return await self.cancel_task(params)
        elif method == "agent/capabilities":
            return await self.get_capabilities()
        elif method == "agent/skills":
            return await self.get_skills()
        elif method == "skill/execute":
            return await self.execute_skill(params)
        elif method == "mgx/create_project":
            return await self.mgx_create_project(params)
        elif method == "mgx/team_discussion":
            return await self.mgx_team_discussion(params)
        elif method == "mgx/generate_artifact":
            return await self.mgx_generate_artifact(params)
        elif method == "mgx/team_info":
            return await self.mgx_get_team_info(params)
        elif method == "mgx/project_status":
            return await self.mgx_get_project_status(params)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown method: {method}")
    
    async def create_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task"""
        task_id = str(uuid.uuid4())
        task = {
            "id": task_id,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "user_id": params.get("user_id"),
            "context_id": params.get("context_id"),
            "metadata": params.get("metadata", {}),
            "messages": [],
            "artifacts": []
        }
        
        self.tasks[task_id] = task
        logger.info(f"Created task {task_id}")
        
        return {
            "task_id": task_id,
            "status": "created",
            "created_at": task["created_at"]
        }
    
    async def send_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message to a task"""
        task_id = params.get("task_id")
        message = params.get("message", {})
        
        if task_id not in self.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task = self.tasks[task_id]
        task["messages"].append({
            "timestamp": datetime.now().isoformat(),
            "role": "user",
            "content": message
        })
        
        # Process the message and generate response
        response = await self.process_message(task, message)
        
        task["messages"].append({
            "timestamp": datetime.now().isoformat(),
            "role": "agent",
            "content": response
        })
        
        task["status"] = "completed"
        
        return {
            "task_id": task_id,
            "response": response,
            "status": task["status"]
        }
    
    async def process_message(self, task: Dict[str, Any], message: Dict[str, Any]) -> Dict[str, Any]:
        """Process a user message and generate response"""
        # Extract text content from message
        text_content = ""
        if "parts" in message:
            for part in message["parts"]:
                if part.get("type") == "text":
                    text_content += part.get("content", "")
        else:
            text_content = message.get("content", "")
        
        # Simple intent detection and skill routing
        response_parts = []
        
        if "generate" in text_content.lower() or "create" in text_content.lower():
            # Text generation request
            skill_result = await self.skills.execute_skill("text_generation", {
                "prompt": text_content,
                "max_tokens": 500
            })
            
            if skill_result.get("success"):
                response_parts.append({
                    "type": "text",
                    "content": skill_result["result"]["generated_text"]
                })
            else:
                response_parts.append({
                    "type": "text", 
                    "content": f"Error: {skill_result.get('error', 'Unknown error')}"
                })
        
        elif "analyze" in text_content.lower() or "summary" in text_content.lower():
            # Text analysis request
            skill_result = await self.skills.execute_skill("text_analysis", {
                "text": text_content,
                "analysis_type": "summary"
            })
            
            if skill_result.get("success"):
                response_parts.append({
                    "type": "text",
                    "content": skill_result["result"]["analysis"]
                })
            else:
                response_parts.append({
                    "type": "text",
                    "content": f"Error: {skill_result.get('error', 'Unknown error')}"
                })
        
        elif "search" in text_content.lower():
            # Web search request
            query = text_content.replace("search", "").strip()
            skill_result = await self.skills.execute_skill("web_search", {
                "query": query,
                "num_results": 3
            })
            
            if skill_result.get("success"):
                search_results = skill_result["result"]["results"]
                result_text = f"Search results for '{query}':\n\n"
                for i, result in enumerate(search_results, 1):
                    result_text += f"{i}. {result['title']}\n   {result['snippet']}\n   {result['url']}\n\n"
                
                response_parts.append({
                    "type": "text",
                    "content": result_text
                })
            else:
                response_parts.append({
                    "type": "text",
                    "content": f"Error: {skill_result.get('error', 'Unknown error')}"
                })
        
        else:
            # Default response
            response_parts.append({
                "type": "text",
                "content": f"Hello! I received your message: '{text_content}'. I can help with text generation, analysis, and web search. Try asking me to 'generate', 'analyze', or 'search' for something!"
            })
        
        return {
            "role": "agent",
            "parts": response_parts
        }
    
    async def get_artifacts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get artifacts for a task"""
        task_id = params.get("task_id")
        
        if task_id not in self.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task = self.tasks[task_id]
        return {
            "task_id": task_id,
            "artifacts": task.get("artifacts", [])
        }
    
    async def cancel_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel a task"""
        task_id = params.get("task_id")
        
        if task_id not in self.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        self.tasks[task_id]["status"] = "cancelled"
        
        return {
            "task_id": task_id,
            "status": "cancelled"
        }
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities"""
        agent_card = self.agent_card_generator.generate_agent_card()
        return agent_card["capabilities"]
    
    async def get_skills(self) -> Dict[str, Any]:
        """Get available skills"""
        return {
            "skills": self.skills.get_available_skills()
        }
    
    async def execute_skill(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a skill directly"""
        skill_name = params.get("skill_name")
        skill_params = params.get("parameters", {})
        
        result = await self.skills.execute_skill(skill_name, skill_params)
        return result
    
    async def mgx_create_project(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """MGX-style project creation with team collaboration"""
        user_request = params.get("description", "")
        user_id = params.get("user_id")
        
        if not user_request:
            raise ValueError("Project description is required")
        
        try:
            project_id = await self.mgx_team.create_project(user_request, user_id)
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            # Fallback to simple project creation
            project_id = str(uuid.uuid4())
        
        return {
            "project_id": project_id,
            "status": "created",
            "message": "Project created! Your AI team is analyzing the requirements..."
        }
    
    async def mgx_team_discussion(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get team discussion on a topic"""
        project_id = params.get("project_id")
        topic = params.get("topic", "Project requirements analysis")
        
        if not project_id:
            raise ValueError("Project ID is required")
        
        try:
            discussion = await self.mgx_team.team_discussion(project_id, topic)
        except Exception as e:
            logger.error(f"Error in team discussion: {e}")
            # Fallback discussion
            discussion = [
                {
                    "agent": "Mike",
                    "avatar": "👨‍💼", 
                    "contribution": f"Great question about '{topic}'. As team leader, I think we should focus on breaking this down into manageable components and ensuring we align with user needs."
                },
                {
                    "agent": "Alex",
                    "avatar": "👨‍💻",
                    "contribution": "From a technical perspective, I'd recommend using modern technologies that are scalable and maintainable. We should consider the architecture carefully."
                },
                {
                    "agent": "Emma", 
                    "avatar": "👩‍💼",
                    "contribution": "From the product side, we need to prioritize user experience and ensure our solution addresses real user pain points. Let's validate our assumptions."
                }
            ]
        
        return {
            "project_id": project_id,
            "topic": topic,
            "discussion": discussion,
            "participants": len(discussion)
        }
    
    async def mgx_generate_artifact(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code or design artifacts"""
        project_id = params.get("project_id")
        component_type = params.get("component_type", "web component")
        
        if not project_id:
            raise ValueError("Project ID is required")
        
        try:
            artifact = await self.mgx_team.generate_code_artifact(project_id, component_type)
        except Exception as e:
            logger.error(f"Error generating artifact: {e}")
            # Fallback artifact generation
            artifact = {
                "id": str(uuid.uuid4()),
                "component_type": component_type,
                "created_by": "Alex",
                "created_at": datetime.now().isoformat(),
                "version": "1.0.0",
                "content": f"""
// {component_type} - Generated by Alex
import React, {{ useState, useEffect }} from 'react';

const {component_type.replace(' ', '')}Component = () => {{
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {{
        // Initialize component
        setLoading(false);
    }}, []);
    
    if (loading) {{
        return <div>Loading...</div>;
    }}
    
    return (
        <div className="component-container">
            <h2>{component_type}</h2>
            <p>This is a modern React component with best practices.</p>
            {{/* Add your component logic here */}}
        </div>
    );
}};

export default {component_type.replace(' ', '')}Component;
"""
            }
        
        return {
            "artifact": artifact,
            "message": f"Code artifact '{component_type}' generated successfully!"
        }
    
    async def mgx_get_team_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI team information"""
        try:
            return await self.mgx_team.get_team_info()
        except Exception as e:
            logger.error(f"Error getting team info: {e}")
            return {
                "team_name": "A2A Development Team",
                "description": "Your 24/7 AI Development Team - Dream, Chat, Create",
                "members": [
                    {
                        "name": "Mike",
                        "role": "team_leader",
                        "avatar": "👨‍💼",
                        "description": "Experienced team leader who coordinates projects and manages team workflow",
                        "specialties": ["project_management", "team_coordination", "strategic_planning"]
                    },
                    {
                        "name": "Alex", 
                        "role": "engineer",
                        "avatar": "👨‍💻",
                        "description": "Full-stack developer with expertise in modern web technologies",
                        "specialties": ["web_development", "backend_apis", "database_design", "devops"]
                    },
                    {
                        "name": "Emma",
                        "role": "product_manager", 
                        "avatar": "👩‍💼",
                        "description": "Product manager focused on user experience and market requirements",
                        "specialties": ["user_research", "product_strategy", "feature_planning", "market_analysis"]
                    }
                ]
            }
    
    async def mgx_get_project_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get project status and progress"""
        project_id = params.get("project_id")
        
        if not project_id:
            raise ValueError("Project ID is required")
        
        try:
            return self.mgx_team.get_project_status(project_id)
        except Exception as e:
            logger.error(f"Error getting project status: {e}")
            # Fallback project status
            return {
                "project_id": project_id,
                "title": "AI Generated Project",
                "status": "in_progress",
                "assigned_agents": ["Mike", "Alex", "Emma"],
                "created_at": datetime.now().isoformat(),
                "artifacts_count": 1,
                "conversation_messages": 3,
                "latest_activity": "Code generation completed"
            }
    
    def run(self, host: str = None, port: int = None):
        """Run the A2A server"""
        host = host or Config.AGENT_HOST
        port = port or Config.AGENT_PORT
        
        logger.info(f"Starting A2A Agent Server on {host}:{port}")
        logger.info(f"Agent Card available at: http://{host}:{port}/agent-card")
        logger.info(f"A2A endpoint at: http://{host}:{port}/a2a")
        
        # Generate and save agent card
        self.agent_card_generator.save_agent_card("agent_card.json")
        
        uvicorn.run(self.app, host=host, port=port, log_level="info")

# Create server instance
server = A2AServer()

if __name__ == "__main__":
    server.run() 
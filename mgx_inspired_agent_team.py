"""
MGX-Inspired Multi-Agent Team System for A2A Protocol
Based on analysis of https://mgx.dev/
"""
import asyncio
import json
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import openai
from config import get_openai_client

class AgentRole(Enum):
    TEAM_LEADER = "team_leader"
    ENGINEER = "engineer" 
    PRODUCT_MANAGER = "product_manager"
    DATA_ANALYST = "data_analyst"
    ARCHITECT = "architect"
    UI_DESIGNER = "ui_designer"

@dataclass
class AgentProfile:
    name: str
    role: AgentRole
    description: str
    specialties: List[str]
    avatar: str
    personality: str

@dataclass 
class ProjectTask:
    id: str
    title: str
    description: str
    requirements: List[str]
    assigned_agents: List[AgentRole]
    status: str
    created_at: datetime
    artifacts: List[Dict[str, Any]]

class MGXInspiredAgentTeam:
    def __init__(self):
        self.client = get_openai_client()
        self.agents = self._initialize_agents()
        self.active_projects: Dict[str, ProjectTask] = {}
        self.conversation_history: Dict[str, List[Dict]] = {}
    
    def _initialize_agents(self) -> Dict[AgentRole, AgentProfile]:
        """Initialize the AI agent team inspired by MGX"""
        return {
            AgentRole.TEAM_LEADER: AgentProfile(
                name="Mike",
                role=AgentRole.TEAM_LEADER,
                description="Experienced team leader who coordinates projects and manages team workflow",
                specialties=["project_management", "team_coordination", "strategic_planning"],
                avatar="👨‍💼",
                personality="Professional, organized, and strategic thinker"
            ),
            AgentRole.ENGINEER: AgentProfile(
                name="Alex",
                role=AgentRole.ENGINEER,
                description="Full-stack developer with expertise in modern web technologies",
                specialties=["web_development", "backend_apis", "database_design", "devops"],
                avatar="👨‍💻",
                personality="Detail-oriented, problem-solver, loves clean code"
            ),
            AgentRole.PRODUCT_MANAGER: AgentProfile(
                name="Emma",
                role=AgentRole.PRODUCT_MANAGER,
                description="Product manager focused on user experience and market requirements",
                specialties=["user_research", "product_strategy", "feature_planning", "market_analysis"],
                avatar="👩‍💼",
                personality="User-focused, analytical, great communicator"
            ),
            AgentRole.DATA_ANALYST: AgentProfile(
                name="David",
                role=AgentRole.DATA_ANALYST,
                description="Data scientist who provides insights and analytics solutions",
                specialties=["data_analysis", "machine_learning", "statistics", "visualization"],
                avatar="👨‍🔬",
                personality="Curious, methodical, data-driven decision maker"
            ),
            AgentRole.ARCHITECT: AgentProfile(
                name="Bob",
                role=AgentRole.ARCHITECT,
                description="System architect who designs scalable and robust solutions",
                specialties=["system_design", "architecture_patterns", "scalability", "security"],
                avatar="👨‍🏗️",
                personality="Big-picture thinker, focuses on long-term solutions"
            ),
            AgentRole.UI_DESIGNER: AgentProfile(
                name="Sophia",
                role=AgentRole.UI_DESIGNER,
                description="UI/UX designer who creates beautiful and intuitive interfaces",
                specialties=["ui_design", "ux_research", "prototyping", "user_interface"],
                avatar="👩‍🎨",
                personality="Creative, user-empathetic, detail-oriented about aesthetics"
            )
        }
    
    async def create_project(self, user_request: str, user_id: Optional[str] = None) -> str:
        """Create a new project based on user request - MGX style"""
        project_id = str(uuid.uuid4())
        
        # Mike (Team Leader) analyzes the request first
        analysis = await self._agent_analyze_request(user_request, AgentRole.TEAM_LEADER)
        
        project = ProjectTask(
            id=project_id,
            title=analysis.get("title", "New Project"),
            description=user_request,
            requirements=analysis.get("requirements", []),
            assigned_agents=analysis.get("assigned_agents", []),
            status="planning",
            created_at=datetime.now(),
            artifacts=[]
        )
        
        self.active_projects[project_id] = project
        self.conversation_history[project_id] = []
        
        return project_id
    
    async def _agent_analyze_request(self, request: str, agent_role: AgentRole) -> Dict[str, Any]:
        """Have a specific agent analyze the user request"""
        agent = self.agents[agent_role]
        
        system_prompt = f"""You are {agent.name}, the {agent.role.value} of an AI development team.
        
Role: {agent.description}
Specialties: {', '.join(agent.specialties)}
Personality: {agent.personality}

Analyze the following user request and provide:
1. A clear project title
2. List of key requirements
3. Which team members should be involved (choose from: team_leader, engineer, product_manager, data_analyst, architect, ui_designer)
4. Initial project scope assessment

Respond in JSON format."""
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User Request: {request}"}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback parsing
                return {
                    "title": "New Project",
                    "requirements": [request],
                    "assigned_agents": [AgentRole.ENGINEER.value, AgentRole.TEAM_LEADER.value],
                    "scope": "To be determined"
                }
                
        except Exception as e:
            print(f"Error in agent analysis: {e}")
            return {
                "title": "New Project", 
                "requirements": [request],
                "assigned_agents": [AgentRole.ENGINEER.value],
                "scope": "Basic implementation"
            }
    
    async def team_discussion(self, project_id: str, topic: str) -> List[Dict[str, Any]]:
        """Simulate team discussion MGX-style"""
        if project_id not in self.active_projects:
            raise ValueError("Project not found")
        
        project = self.active_projects[project_id]
        responses = []
        
        # Each assigned agent contributes to the discussion
        for agent_role_str in project.assigned_agents:
            try:
                agent_role = AgentRole(agent_role_str)
                response = await self._agent_contribute(project, topic, agent_role)
                responses.append({
                    "agent": self.agents[agent_role].name,
                    "role": agent_role.value,
                    "avatar": self.agents[agent_role].avatar,
                    "contribution": response,
                    "timestamp": datetime.now().isoformat()
                })
            except ValueError:
                continue
        
        # Add to conversation history
        self.conversation_history[project_id].extend(responses)
        return responses
    
    async def _agent_contribute(self, project: ProjectTask, topic: str, agent_role: AgentRole) -> str:
        """Get contribution from a specific agent"""
        agent = self.agents[agent_role]
        
        # Get relevant conversation context
        recent_context = self.conversation_history.get(project.id, [])[-5:]  # Last 5 messages
        context_str = "\n".join([f"{msg['agent']}: {msg['contribution']}" for msg in recent_context])
        
        system_prompt = f"""You are {agent.name}, the {agent.role.value}.
        
Role: {agent.description}
Specialties: {', '.join(agent.specialties)}
Personality: {agent.personality}

Project: {project.title}
Description: {project.description}

Recent team discussion:
{context_str}

Provide your professional input on: {topic}

Keep your response concise, focused on your expertise, and collaborative."""
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Topic for discussion: {topic}"}
                ],
                temperature=0.8,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"[{agent.name} is temporarily unavailable: {str(e)}]"
    
    async def generate_code_artifact(self, project_id: str, component_type: str) -> Dict[str, Any]:
        """Generate code artifacts like MGX does"""
        if project_id not in self.active_projects:
            raise ValueError("Project not found")
        
        project = self.active_projects[project_id]
        
        # Alex (Engineer) generates the code
        code_content = await self._agent_generate_code(project, component_type)
        
        artifact = {
            "id": str(uuid.uuid4()),
            "type": "code",
            "component_type": component_type,
            "content": code_content,
            "created_by": "Alex",
            "created_at": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        project.artifacts.append(artifact)
        return artifact
    
    async def _agent_generate_code(self, project: ProjectTask, component_type: str) -> str:
        """Alex generates code based on project requirements"""
        alex = self.agents[AgentRole.ENGINEER]
        
        system_prompt = f"""You are {alex.name}, the {alex.role.value}.
        
Project: {project.title}
Requirements: {', '.join(project.requirements)}

Generate clean, modern {component_type} code for this project.
Follow best practices and include helpful comments.
Make it production-ready and well-structured."""
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate {component_type} for: {project.description}"}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"// Error generating code: {str(e)}"
    
    def get_team_info(self) -> Dict[str, Any]:
        """Get team information MGX-style"""
        team_info = {
            "team_name": "A2A Development Team",
            "description": "Your 24/7 AI Development Team - Dream, Chat, Create",
            "members": []
        }
        
        for role, agent in self.agents.items():
            team_info["members"].append({
                "name": agent.name,
                "role": agent.role.value,
                "avatar": agent.avatar,
                "description": agent.description,
                "specialties": agent.specialties
            })
        
        return team_info
    
    def get_project_status(self, project_id: str) -> Dict[str, Any]:
        """Get project status and artifacts"""
        if project_id not in self.active_projects:
            raise ValueError("Project not found")
        
        project = self.active_projects[project_id]
        
        return {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "status": project.status,
            "assigned_agents": project.assigned_agents,
            "created_at": project.created_at.isoformat(),
            "artifacts_count": len(project.artifacts),
            "conversation_messages": len(self.conversation_history.get(project_id, [])),
            "latest_activity": self.conversation_history.get(project_id, [{}])[-1].get("timestamp") if self.conversation_history.get(project_id) else None
        }

# Usage example
async def demo_mgx_inspired_team():
    """Demo the MGX-inspired team functionality"""
    team = MGXInspiredAgentTeam()
    
    print("=== A2A Team Info ===")
    team_info = team.get_team_info()
    print(f"Team: {team_info['team_name']}")
    print(f"Description: {team_info['description']}")
    print("\nTeam Members:")
    for member in team_info['members']:
        print(f"{member['avatar']} {member['name']} - {member['role']}")
        print(f"   {member['description']}")
        print(f"   Specialties: {', '.join(member['specialties'])}")
        print()
    
    # Create a project
    print("=== Creating Project ===")
    project_id = await team.create_project(
        "Create a modern to-do list web application with user authentication and real-time collaboration"
    )
    print(f"Project created: {project_id}")
    
    # Team discussion
    print("\n=== Team Discussion ===")
    discussion = await team.team_discussion(project_id, "Let's plan the architecture and tech stack")
    for response in discussion:
        print(f"{response['avatar']} {response['agent']}: {response['contribution']}")
        print()
    
    # Generate code artifact
    print("=== Generating Code ===")
    artifact = await team.generate_code_artifact(project_id, "React component")
    print(f"Code artifact generated by {artifact['created_by']}")
    print("Preview:")
    print(artifact['content'][:200] + "...")
    
    # Project status
    print("\n=== Project Status ===")
    status = team.get_project_status(project_id)
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    asyncio.run(demo_mgx_inspired_team()) 
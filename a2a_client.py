"""
A2A Protocol Client Implementation
"""
import requests
import json
import uuid
from typing import Dict, Any, Optional, List
import asyncio
import aiohttp
from datetime import datetime

class A2AClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize A2A Client
        
        Args:
            base_url: Base URL of the A2A agent (e.g., "http://localhost:8000")
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.a2a_endpoint = f"{self.base_url}/a2a"
        self.agent_card_url = f"{self.base_url}/agent-card"
        self.api_key = api_key
        
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def get_agent_card(self) -> Dict[str, Any]:
        """Get the agent card from the remote agent"""
        try:
            response = requests.get(self.agent_card_url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to get agent card: {str(e)}")
    
    def send_jsonrpc_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a JSON-RPC 2.0 request to the A2A endpoint"""
        request_id = str(uuid.uuid4())
        
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": request_id
        }
        
        if params:
            payload["params"] = params
        
        try:
            response = requests.post(
                self.a2a_endpoint, 
                json=payload, 
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            if "error" in result:
                raise Exception(f"A2A Error: {result['error']}")
            
            return result.get("result", {})
            
        except requests.RequestException as e:
            raise Exception(f"Failed to send A2A request: {str(e)}")
    
    def create_task(self, user_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Create a new task and return task ID"""
        params = {}
        if user_id:
            params["user_id"] = user_id
        if metadata:
            params["metadata"] = metadata
        
        result = self.send_jsonrpc_request("task/create", params)
        return result["task_id"]
    
    def send_message(self, task_id: str, message: str) -> Dict[str, Any]:
        """Send a message to a task"""
        message_data = {
            "role": "user",
            "parts": [
                {
                    "type": "text",
                    "content": message
                }
            ]
        }
        
        params = {
            "task_id": task_id,
            "message": message_data
        }
        
        return self.send_jsonrpc_request("task/message", params)
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities"""
        return self.send_jsonrpc_request("agent/capabilities")
    
    def get_skills(self) -> List[Dict[str, Any]]:
        """Get available skills"""
        result = self.send_jsonrpc_request("agent/skills")
        return result.get("skills", [])
    
    def execute_skill(self, skill_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific skill"""
        params = {
            "skill_name": skill_name,
            "parameters": parameters
        }
        
        return self.send_jsonrpc_request("skill/execute", params)
    
    def get_artifacts(self, task_id: str) -> List[Dict[str, Any]]:
        """Get artifacts for a task"""
        params = {"task_id": task_id}
        result = self.send_jsonrpc_request("task/artifacts", params)
        return result.get("artifacts", [])
    
    def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """Cancel a task"""
        params = {"task_id": task_id}
        return self.send_jsonrpc_request("task/cancel", params)
    
    def chat_with_agent(self, message: str, user_id: Optional[str] = None) -> str:
        """Simple chat interface - creates task, sends message, returns response"""
        try:
            # Create task
            task_id = self.create_task(user_id=user_id)
            
            # Send message
            response = self.send_message(task_id, message)
            
            # Extract text response
            agent_response = response.get("response", {})
            if "parts" in agent_response:
                text_parts = [
                    part.get("content", "") 
                    for part in agent_response["parts"] 
                    if part.get("type") == "text"
                ]
                return "\n".join(text_parts)
            
            return str(agent_response)
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """Test if the agent is reachable and responding"""
        try:
            agent_card = self.get_agent_card()
            return bool(agent_card.get("identity", {}).get("name"))
        except:
            return False
    
    def print_agent_info(self):
        """Print agent information"""
        try:
            agent_card = self.get_agent_card()
            identity = agent_card.get("identity", {})
            capabilities = agent_card.get("capabilities", {})
            
            print(f"=== Agent Information ===")
            print(f"Name: {identity.get('name', 'Unknown')}")
            print(f"Description: {identity.get('description', 'No description')}")
            print(f"Version: {identity.get('version', 'Unknown')}")
            print(f"Author: {identity.get('author', 'Unknown')}")
            print(f"\n=== Capabilities ===")
            for cap, enabled in capabilities.items():
                print(f"- {cap}: {'[OK]' if enabled else '[NO]'}")
            
            print(f"\n=== Available Skills ===")
            skills = self.get_skills()
            for skill in skills:
                print(f"- {skill['name']}: {skill['description']}")
                
        except Exception as e:
            print(f"Error getting agent info: {str(e)}")

# Async version for advanced use cases
class AsyncA2AClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.a2a_endpoint = f"{self.base_url}/a2a"
        self.agent_card_url = f"{self.base_url}/agent-card"
        self.api_key = api_key
        
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    async def send_jsonrpc_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send async JSON-RPC request"""
        request_id = str(uuid.uuid4())
        
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": request_id
        }
        
        if params:
            payload["params"] = params
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    self.a2a_endpoint,
                    json=payload,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    
                    if "error" in result:
                        raise Exception(f"A2A Error: {result['error']}")
                    
                    return result.get("result", {})
                    
            except aiohttp.ClientError as e:
                raise Exception(f"Failed to send A2A request: {str(e)}")
    
    async def chat_with_agent(self, message: str, user_id: Optional[str] = None) -> str:
        """Async chat interface"""
        try:
            # Create task
            task_result = await self.send_jsonrpc_request("task/create", {
                "user_id": user_id
            })
            task_id = task_result["task_id"]
            
            # Send message
            message_data = {
                "role": "user",
                "parts": [{"type": "text", "content": message}]
            }
            
            response = await self.send_jsonrpc_request("task/message", {
                "task_id": task_id,
                "message": message_data
            })
            
            # Extract response
            agent_response = response.get("response", {})
            if "parts" in agent_response:
                text_parts = [
                    part.get("content", "") 
                    for part in agent_response["parts"] 
                    if part.get("type") == "text"
                ]
                return "\n".join(text_parts)
            
            return str(agent_response)
            
        except Exception as e:
            return f"Error: {str(e)}"

# Example usage and testing
if __name__ == "__main__":
    # Test the client
    client = A2AClient("http://localhost:8000")
    
    if client.test_connection():
        print("[OK] Successfully connected to A2A agent!")
        client.print_agent_info()
        
        print("\n=== Testing Chat ===")
        
        # Test different types of requests
        test_messages = [
            "Hello, can you introduce yourself?",
            "Generate a short poem about artificial intelligence",
            "Analyze this text: 'AI is transforming the world rapidly'",
            "Search for information about machine learning"
        ]
        
        for message in test_messages:
            print(f"\nUser: {message}")
            response = client.chat_with_agent(message)
            print(f"Agent: {response}")
    else:
        print("[ERROR] Failed to connect to A2A agent. Make sure the server is running.") 
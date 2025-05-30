#!/usr/bin/env python3
"""
Crew Sync Agent - Multi-Team AI Collaboration MCP Server
Dynamic team collaboration system for Smithery deployment

Default Crew Members (expandable):
🎯 Taylor - Team Coordinator (Project coordination, strategic planning)
⚡ Jordan - Tech Engineer (Full-stack development, DevOps)  
💡 Riley - Product Strategist (UX research, feature planning)
📊 Casey - Data Specialist (ML, analytics, visualization)
🏗️ Morgan - System Architect (System design, scalability)
🎨 Avery - Design Lead (Interface design, prototyping)

Note: Crew size and composition can be dynamically adjusted
"""

import asyncio
import json
import logging
import os
from typing import Any, List, Optional, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("crew-sync-agent")

class CrewSyncAgent:
    def __init__(self):
        # Default crew members (can be expanded)
        self.default_crew = {
            "Taylor": "🎯 Team Coordinator - Strategic planning and project coordination",
            "Jordan": "⚡ Tech Engineer - Technical implementation and DevOps", 
            "Riley": "💡 Product Strategist - User experience design and feature planning",
            "Casey": "📊 Data Specialist - Analytics, insights, and ML operations",
            "Morgan": "🏗️ System Architect - System design and scalability",
            "Avery": "🎨 Design Lead - Interface design and prototyping"
        }
        
        # Maximum crew size from environment or default
        self.max_crew_size = int(os.getenv("MAX_CREW_SIZE", "10"))
        
        self.tools = [
            {
                "name": "sync_crew",
                "description": "Synchronize multiple crew members for collaborative problem solving",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "Task description for the crew collaboration"
                        },
                        "crew_members": {
                            "type": "array",
                            "description": f"Crew members to involve (max {self.max_crew_size}). Available: {', '.join(self.default_crew.keys())}",
                            "items": {"type": "string"},
                            "maxItems": self.max_crew_size
                        },
                        "priority": {
                            "type": "string",
                            "description": "Task priority level",
                            "enum": ["low", "medium", "high", "urgent"]
                        }
                    },
                    "required": ["task"]
                }
            },
            {
                "name": "add_crew_member",
                "description": "Dynamically add a new crew member with specific role",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the new crew member"
                        },
                        "role": {
                            "type": "string",
                            "description": "Role and expertise description"
                        }
                    },
                    "required": ["name", "role"]
                }
            },
            {
                "name": "list_crew",
                "description": "List all available crew members and their roles",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "echo",
                "description": "Echo back the input text (for testing)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to echo back"
                        }
                    },
                    "required": ["text"]
                }
            }
        ]
        
    async def handle_initialize(self, params: dict) -> dict:
        """Handle initialization request"""
        logger.info("Initializing Crew Sync Agent MCP server")
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {},
                "prompts": {}
            },
            "serverInfo": {
                "name": "crew-sync-agent",
                "version": "1.0.0"
            }
        }
    
    async def handle_list_tools(self, params: dict) -> dict:
        """Handle tools/list request"""
        logger.info("Listing crew synchronization tools")
        return {
            "tools": self.tools
        }
    
    async def handle_call_tool(self, params: dict) -> dict:
        """Handle tools/call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        logger.info(f"Calling tool: {tool_name} with args: {arguments}")
        
        if tool_name == "sync_crew":
            task = arguments.get("task", "")
            crew_members = arguments.get("crew_members", list(self.default_crew.keys()))
            priority = arguments.get("priority", "medium")
            
            # Limit crew size
            if len(crew_members) > self.max_crew_size:
                crew_members = crew_members[:self.max_crew_size]
            
            # Generate collaborative response
            response_parts = [
                f"🔄 Crew Sync Agent - {priority.upper()} Priority",
                f"📋 Task: {task}",
                f"👥 Active Crew ({len(crew_members)} members):",
                ""
            ]
            
            for member in crew_members:
                if member in self.default_crew:
                    response_parts.append(f"  {self.default_crew[member]}")
                    response_parts.append(f"    ↳ Synchronized for: {task}")
                else:
                    response_parts.append(f"  ❓ {member} - Unknown crew member")
            
            response_parts.extend([
                "",
                f"✅ Crew synchronization complete for {len(crew_members)} members",
                f"🎯 Ready to collaborate on: {task}"
            ])
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "\n".join(response_parts)
                    }
                ]
            }
        
        elif tool_name == "add_crew_member":
            name = arguments.get("name", "")
            role = arguments.get("role", "")
            
            if len(self.default_crew) >= self.max_crew_size:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"❌ Cannot add {name}: Crew size limit ({self.max_crew_size}) reached"
                        }
                    ]
                }
            
            # Add new crew member
            self.default_crew[name] = f"🆕 {role}"
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"✅ {name} added to crew!\n🆕 Role: {role}\n👥 Total crew members: {len(self.default_crew)}"
                    }
                ]
            }
        
        elif tool_name == "list_crew":
            crew_list = [
                f"👥 Current Crew ({len(self.default_crew)}/{self.max_crew_size} members):",
                "=" * 50
            ]
            
            for name, role in self.default_crew.items():
                crew_list.append(f"• {name}: {role}")
            
            crew_list.extend([
                "=" * 50,
                f"💡 Use 'add_crew_member' to expand the team (max {self.max_crew_size})"
            ])
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "\n".join(crew_list)
                    }
                ]
            }
        
        elif tool_name == "echo":
            text = arguments.get("text", "")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Crew Sync Echo: {text}"
                    }
                ]
            }
        
        else:
            raise Exception(f"Unknown tool: {tool_name}")
    
    async def handle_request(self, request: dict) -> dict:
        """Handle incoming JSON-RPC request"""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "initialize":
            result = await self.handle_initialize(params)
        elif method == "tools/list":
            result = await self.handle_list_tools(params)
        elif method == "tools/call":
            result = await self.handle_call_tool(params)
        else:
            raise Exception(f"Unknown method: {method}")
            
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": result
        }

async def main():
    """Main MCP server loop using stdio"""
    import sys
    
    server = CrewSyncAgent()
    logger.info("Starting Crew Sync Agent MCP server...")
    
    try:
        while True:
            # Read line from stdin
            line = sys.stdin.readline()
            if not line:
                break
                
            line = line.strip()
            if not line:
                continue
                
            try:
                # Parse JSON-RPC request
                request = json.loads(line)
                logger.info(f"Received request: {request}")
                
                # Handle request
                response = await server.handle_request(request)
                
                # Send response to stdout
                response_json = json.dumps(response)
                print(response_json)
                sys.stdout.flush()
                
                logger.info(f"Sent response: {response}")
                
            except Exception as e:
                # Send error response
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if 'request' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
                logger.error(f"Error handling request: {e}")
                
    except Exception as e:
        logger.error(f"Server error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code) 
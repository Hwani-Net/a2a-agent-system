#!/usr/bin/env python3
"""
Simple MCP Server for A2A Agent System
Basic working implementation for Smithery deployment
"""

import asyncio
import json
import logging
from typing import Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("a2a-mcp-server")

# Simplified MCP implementation
class MCPServer:
    def __init__(self):
        self.tools = [
            {
                "name": "echo",
                "description": "Echo back the input text",
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
            },
            {
                "name": "add",
                "description": "Add two numbers",
                "inputSchema": {
                    "type": "object", 
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "First number"
                        },
                        "b": {
                            "type": "number", 
                            "description": "Second number"
                        }
                    },
                    "required": ["a", "b"]
                }
            }
        ]
        
    async def handle_initialize(self, params: dict) -> dict:
        """Handle initialization request"""
        logger.info("Initializing MCP server")
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {},
                "prompts": {}
            },
            "serverInfo": {
                "name": "a2a-agent-system",
                "version": "1.0.0"
            }
        }
    
    async def handle_list_tools(self, params: dict) -> dict:
        """Handle tools/list request"""
        logger.info("Listing tools")
        return {
            "tools": self.tools
        }
    
    async def handle_call_tool(self, params: dict) -> dict:
        """Handle tools/call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        logger.info(f"Calling tool: {tool_name} with args: {arguments}")
        
        if tool_name == "echo":
            text = arguments.get("text", "")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Echo: {text}"
                    }
                ]
            }
        
        elif tool_name == "add":
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            result = a + b
            return {
                "content": [
                    {
                        "type": "text", 
                        "text": f"Result: {a} + {b} = {result}"
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
    
    server = MCPServer()
    logger.info("Starting MCP server...")
    
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
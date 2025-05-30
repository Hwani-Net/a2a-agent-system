#!/usr/bin/env python3
"""
Test script for MCP server
"""

import json
import subprocess
import sys

def test_mcp_server():
    """Test MCP server with basic requests"""
    print("🧪 MCP 서버 테스트 시작\n")
    
    # Test requests
    tests = [
        {
            "name": "Initialize",
            "request": {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {}
            }
        },
        {
            "name": "List Tools",
            "request": {
                "jsonrpc": "2.0", 
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
        },
        {
            "name": "Echo Tool",
            "request": {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "echo",
                    "arguments": {
                        "text": "Hello Smithery!"
                    }
                }
            }
        },
        {
            "name": "Add Tool",
            "request": {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call", 
                "params": {
                    "name": "add",
                    "arguments": {
                        "a": 5,
                        "b": 3
                    }
                }
            }
        }
    ]
    
    for test in tests:
        print(f"🔍 {test['name']} 테스트...")
        
        try:
            # Convert request to JSON string
            request_json = json.dumps(test['request'])
            
            # Run MCP server with the request
            process = subprocess.run(
                [sys.executable, "mcp_server.py"],
                input=request_json,
                text=True,
                capture_output=True,
                timeout=10
            )
            
            if process.returncode == 0:
                print(f"  ✅ 성공")
                # Parse response if available
                try:
                    response = json.loads(process.stdout.strip().split('\n')[-1])
                    if 'result' in response:
                        if test['name'] == "Echo Tool":
                            content = response['result'].get('content', [])
                            if content and len(content) > 0:
                                print(f"  📝 응답: {content[0].get('text', '')}")
                        elif test['name'] == "Add Tool":
                            content = response['result'].get('content', [])
                            if content and len(content) > 0:
                                print(f"  🔢 응답: {content[0].get('text', '')}")
                        elif test['name'] == "List Tools":
                            tools = response['result'].get('tools', [])
                            print(f"  🛠️ 도구 수: {len(tools)}")
                            for tool in tools:
                                print(f"    - {tool.get('name')}: {tool.get('description')}")
                        elif test['name'] == "Initialize":
                            server_info = response['result'].get('serverInfo', {})
                            print(f"  📡 서버: {server_info.get('name')} v{server_info.get('version')}")
                except:
                    print(f"  📄 원시 응답: {process.stdout.strip()}")
            else:
                print(f"  ❌ 실패")
                print(f"  🚨 오류: {process.stderr}")
                
        except Exception as e:
            print(f"  ❌ 예외 발생: {e}")
        
        print()
    
    print("🎉 MCP 서버 테스트 완료!")

if __name__ == "__main__":
    test_mcp_server() 
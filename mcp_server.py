#!/usr/bin/env python3
"""
A2A Agent System MCP Server
Model Context Protocol 표준을 따르는 A2A 에이전트 시스템 서버
"""

import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from skills import SkillManager
from agent_card import A2AAgentCard

# MCP 서버 설정
MCP_VERSION = "2024-11-05"
SERVER_NAME = "a2a-agent-system"
SERVER_VERSION = "1.0.0"

class MCPServer:
    """A2A Agent System MCP Server"""
    
    def __init__(self):
        self.config = Config()
        self.skill_manager = SkillManager(self.config)
        self.agent_card = A2AAgentCard()
        self.active_sessions = {}
        
        # MCP 메서드 등록
        self.methods = {
            "initialize": self.initialize,
            "tools/list": self.list_tools,
            "tools/call": self.call_tool,
            "resources/list": self.list_resources,
            "resources/read": self.read_resource,
            "prompts/list": self.list_prompts,
            "prompts/get": self.get_prompt,
            "ping": self.ping,
            "notifications/initialized": self.notifications_initialized
        }
        
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """로깅 설정"""
        logger = logging.getLogger("a2a_mcp_server")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    async def initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """MCP 초기화"""
        self.logger.info("A2A MCP Server 초기화 중...")
        
        return {
            "protocolVersion": MCP_VERSION,
            "capabilities": {
                "tools": {
                    "listChanged": True
                },
                "resources": {
                    "subscribe": True,
                    "listChanged": True
                },
                "prompts": {
                    "listChanged": True
                },
                "experimental": {}
            },
            "serverInfo": {
                "name": SERVER_NAME,
                "version": SERVER_VERSION,
                "description": "A2A (Agent2Agent) 호환 AI 에이전트 시스템"
            }
        }
    
    async def list_tools(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """사용 가능한 도구 목록 반환"""
        tools = [
            {
                "name": "generate_text",
                "description": "AI 모델을 사용하여 텍스트를 생성합니다",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "생성할 텍스트에 대한 프롬프트"
                        },
                        "model": {
                            "type": "string",
                            "description": "사용할 AI 모델 (선택사항)",
                            "default": "gpt-3.5-turbo"
                        },
                        "max_tokens": {
                            "type": "integer",
                            "description": "최대 토큰 수",
                            "default": 1000
                        },
                        "temperature": {
                            "type": "number",
                            "description": "생성 온도 (0.0-1.0)",
                            "default": 0.7
                        }
                    },
                    "required": ["prompt"]
                }
            },
            {
                "name": "analyze_text",
                "description": "텍스트를 분석하고 요약, 감정 분석 등을 제공합니다",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "분석할 텍스트"
                        },
                        "analysis_type": {
                            "type": "string",
                            "description": "분석 유형 (summary, sentiment, keywords)",
                            "default": "summary"
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "web_search",
                "description": "웹 검색을 수행합니다",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "검색 쿼리"
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "반환할 결과 수",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_weather",
                "description": "특정 도시의 날씨 정보를 가져옵니다",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "도시 이름"
                        }
                    },
                    "required": ["city"]
                }
            }
        ]
        
        return {"tools": tools}
    
    async def call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """도구 호출 실행"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "generate_text":
                result = await self.skill_manager.generate_text(
                    prompt=arguments["prompt"],
                    model=arguments.get("model", "gpt-3.5-turbo"),
                    max_tokens=arguments.get("max_tokens", 1000),
                    temperature=arguments.get("temperature", 0.7)
                )
            elif tool_name == "analyze_text":
                result = await self.skill_manager.analyze_text(
                    text=arguments["text"],
                    analysis_type=arguments.get("analysis_type", "summary")
                )
            elif tool_name == "web_search":
                result = await self.skill_manager.web_search(
                    query=arguments["query"],
                    num_results=arguments.get("num_results", 5)
                )
            elif tool_name == "get_weather":
                result = await self.skill_manager.get_weather(
                    city=arguments["city"]
                )
            else:
                raise ValueError(f"알 수 없는 도구: {tool_name}")
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, ensure_ascii=False, indent=2)
                    }
                ]
            }
            
        except Exception as e:
            self.logger.error(f"도구 호출 오류 ({tool_name}): {e}")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"오류: {str(e)}"
                    }
                ],
                "isError": True
            }
    
    async def list_resources(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """사용 가능한 리소스 목록"""
        resources = [
            {
                "uri": "agent://card",
                "name": "Agent Card",
                "description": "A2A 에이전트 카드 정보",
                "mimeType": "application/json"
            },
            {
                "uri": "agent://config",
                "name": "Configuration",
                "description": "현재 설정 정보",
                "mimeType": "application/json"
            },
            {
                "uri": "agent://status",
                "name": "Server Status",
                "description": "서버 상태 정보",
                "mimeType": "application/json"
            }
        ]
        
        return {"resources": resources}
    
    async def read_resource(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """리소스 읽기"""
        uri = params.get("uri")
        
        try:
            if uri == "agent://card":
                content = self.agent_card.generate_card()
            elif uri == "agent://config":
                content = {
                    "server_name": SERVER_NAME,
                    "version": SERVER_VERSION,
                    "available_models": self.config.available_models(),
                    "status": "active"
                }
            elif uri == "agent://status":
                content = {
                    "server": "running",
                    "active_sessions": len(self.active_sessions),
                    "uptime": str(datetime.now()),
                    "capabilities": ["text_generation", "text_analysis", "web_search", "weather"]
                }
            else:
                raise ValueError(f"알 수 없는 리소스: {uri}")
            
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(content, ensure_ascii=False, indent=2)
                    }
                ]
            }
            
        except Exception as e:
            self.logger.error(f"리소스 읽기 오류 ({uri}): {e}")
            raise
    
    async def list_prompts(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """사용 가능한 프롬프트 목록"""
        prompts = [
            {
                "name": "code_review",
                "description": "코드 리뷰를 위한 프롬프트",
                "arguments": [
                    {
                        "name": "code",
                        "description": "리뷰할 코드",
                        "required": True
                    },
                    {
                        "name": "language",
                        "description": "프로그래밍 언어",
                        "required": False
                    }
                ]
            },
            {
                "name": "documentation",
                "description": "문서 생성을 위한 프롬프트",
                "arguments": [
                    {
                        "name": "topic",
                        "description": "문서화할 주제",
                        "required": True
                    },
                    {
                        "name": "format",
                        "description": "문서 형식 (markdown, rst, etc.)",
                        "required": False
                    }
                ]
            }
        ]
        
        return {"prompts": prompts}
    
    async def get_prompt(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """프롬프트 가져오기"""
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        if name == "code_review":
            code = arguments.get("code", "")
            language = arguments.get("language", "python")
            
            prompt = f"""다음 {language} 코드를 리뷰해주세요:

```{language}
{code}
```

다음 관점에서 분석해주세요:
1. 코드 품질
2. 성능 최적화 가능성
3. 보안 이슈
4. 개선 제안사항
"""
        
        elif name == "documentation":
            topic = arguments.get("topic", "")
            format_type = arguments.get("format", "markdown")
            
            prompt = f"""'{topic}'에 대한 {format_type} 형식의 문서를 작성해주세요.

다음 구조로 작성해주세요:
1. 개요
2. 주요 기능
3. 사용 방법
4. 예제
5. 참고사항
"""
        
        else:
            raise ValueError(f"알 수 없는 프롬프트: {name}")
        
        return {
            "description": f"{name} 프롬프트",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt
                    }
                }
            ]
        }
    
    async def ping(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """서버 상태 확인"""
        return {"status": "pong", "timestamp": datetime.now().isoformat()}
    
    async def notifications_initialized(self, params: Dict[str, Any]) -> None:
        """초기화 완료 알림"""
        self.logger.info("MCP 클라이언트 초기화 완료")
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """요청 처리"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method in self.methods:
                result = await self.methods[method](params)
                
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                
        except Exception as e:
            self.logger.error(f"요청 처리 오류: {e}")
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
        
        return response
    
    async def start_stdio_server(self):
        """STDIO 기반 MCP 서버 시작"""
        self.logger.info("A2A MCP 서버 시작 (STDIO 모드)")
        
        try:
            while True:
                # STDIN에서 JSON-RPC 메시지 읽기
                line = sys.stdin.readline()
                if not line:
                    break
                
                try:
                    request = json.loads(line.strip())
                    response = await self.handle_request(request)
                    
                    # STDOUT으로 응답 전송
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                    
                except json.JSONDecodeError as e:
                    self.logger.error(f"JSON 파싱 오류: {e}")
                except Exception as e:
                    self.logger.error(f"요청 처리 오류: {e}")
                    
        except KeyboardInterrupt:
            self.logger.info("서버 종료 중...")
        except Exception as e:
            self.logger.error(f"서버 오류: {e}")

async def main():
    """MCP 서버 실행"""
    server = MCPServer()
    await server.start_stdio_server()

if __name__ == "__main__":
    asyncio.run(main()) 
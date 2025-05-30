#!/usr/bin/env python3
"""
A2A Agent System - Simple MCP Server
Working MCP server for Smithery deployment
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Sequence

# 기본 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP 관련 imports - 간단하게 처리
try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    from mcp.types import (
        Tool, TextContent, CallToolResult, 
        ListToolsResult
    )
    from mcp.server.stdio import stdio_server
    logger.info("MCP 패키지 로드 성공")
except ImportError as e:
    logger.error(f"MCP 패키지 오류: {e}")
    # 대체 구현
    class Server:
        def __init__(self, name): 
            self.name = name
        def list_tools(self): 
            return lambda f: f
        def call_tool(self): 
            return lambda f: f
    
    class Tool:
        def __init__(self, **kwargs): 
            self.__dict__.update(kwargs)
    
    class TextContent:
        def __init__(self, **kwargs): 
            self.__dict__.update(kwargs)
    
    class CallToolResult:
        def __init__(self, **kwargs): 
            self.__dict__.update(kwargs)
    
    class ListToolsResult:
        def __init__(self, **kwargs): 
            self.__dict__.update(kwargs)

# 간단한 MCP 서버 클래스
class SimpleMCPServer:
    """간단하고 안정적인 MCP 서버"""
    
    def __init__(self):
        self.server = Server("a2a-agent-system")
        self.setup_tools()
        logger.info("SimpleMCPServer 초기화 완료")
    
    def setup_tools(self):
        """MCP 도구 설정"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """사용 가능한 도구 목록"""
            try:
                tools = [
                    Tool(
                        name="echo",
                        description="Echo back the input text",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "text": {
                                    "type": "string",
                                    "description": "Text to echo back"
                                }
                            },
                            "required": ["text"]
                        }
                    ),
                    Tool(
                        name="get_system_info",
                        description="Get basic system information",
                        inputSchema={
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    ),
                    Tool(
                        name="generate_text",
                        description="Generate text using AI (placeholder)",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "prompt": {
                                    "type": "string",
                                    "description": "Text prompt for generation"
                                },
                                "max_length": {
                                    "type": "integer",
                                    "description": "Maximum length of generated text",
                                    "default": 100
                                }
                            },
                            "required": ["prompt"]
                        }
                    )
                ]
                
                logger.info(f"도구 목록 반환: {len(tools)}개")
                return ListToolsResult(tools=tools)
                
            except Exception as e:
                logger.error(f"도구 목록 생성 오류: {e}")
                return ListToolsResult(tools=[])
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
            """도구 실행"""
            try:
                logger.info(f"도구 호출: {name}, 인수: {arguments}")
                
                if name == "echo":
                    text = arguments.get("text", "")
                    result = f"Echo: {text}"
                    
                elif name == "get_system_info":
                    result = {
                        "server": "A2A MCP Server",
                        "version": "1.0.0",
                        "python_version": sys.version,
                        "platform": sys.platform,
                        "environment_variables": {
                            "OPENAI_API_KEY": "SET" if os.getenv("OPENAI_API_KEY") else "NOT_SET",
                            "ANTHROPIC_API_KEY": "SET" if os.getenv("ANTHROPIC_API_KEY") else "NOT_SET"
                        }
                    }
                    
                elif name == "generate_text":
                    prompt = arguments.get("prompt", "")
                    max_length = arguments.get("max_length", 100)
                    
                    # API 키 확인
                    openai_key = os.getenv("OPENAI_API_KEY")
                    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
                    
                    if openai_key:
                        result = f"[OpenAI] 생성된 텍스트 (프롬프트: '{prompt}'): 이것은 실제 AI 생성 텍스트의 플레이스홀더입니다. 프로덕션에서는 실제 OpenAI API를 호출합니다."
                    elif anthropic_key:
                        result = f"[Anthropic] 생성된 텍스트 (프롬프트: '{prompt}'): 이것은 실제 AI 생성 텍스트의 플레이스홀더입니다. 프로덕션에서는 실제 Anthropic API를 호출합니다."
                    else:
                        result = f"API 키가 설정되지 않았습니다. 프롬프트 '{prompt}'에 대한 응답을 생성하려면 OPENAI_API_KEY 또는 ANTHROPIC_API_KEY를 설정해주세요."
                
                else:
                    result = f"알 수 없는 도구: {name}"
                
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=str(result) if not isinstance(result, str) else result
                        )
                    ]
                )
                
            except Exception as e:
                logger.error(f"도구 실행 오류 {name}: {e}")
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"오류: {str(e)}"
                        )
                    ]
                )

async def main():
    """메인 함수"""
    try:
        logger.info("A2A MCP 서버 시작...")
        
        # 환경변수 로깅 (값은 숨김)
        api_keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "COHERE_API_KEY"]
        for key in api_keys:
            status = "설정됨" if os.getenv(key) else "설정되지 않음"
            logger.info(f"{key}: {status}")
        
        # MCP 서버 생성 및 실행
        server_instance = SimpleMCPServer()
        
        async with stdio_server() as (read_stream, write_stream):
            logger.info("stdio 서버 연결 대기 중...")
            await server_instance.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="a2a-agent-system",
                    server_version="1.0.0",
                    capabilities=server_instance.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )
            
    except KeyboardInterrupt:
        logger.info("서버 종료 요청됨")
    except Exception as e:
        logger.error(f"서버 오류: {e}")
        raise

if __name__ == "__main__":
    # 비동기 메인 함수 실행
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"프로그램 오류: {e}")
        sys.exit(1) 
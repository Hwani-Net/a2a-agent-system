#!/usr/bin/env python3
"""
A2A Agent System - MCP Server Implementation
Smithery 배포를 위한 Model Context Protocol 서버
"""

import asyncio
import json
import logging
import sys
from typing import Any, Sequence, Dict, Optional
import traceback

# MCP 관련 imports
try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    from mcp.types import (
        Resource, Tool, TextContent, ImageContent, EmbeddedResource,
        LoggingLevel, CallToolResult, ListResourcesResult, 
        ListToolsResult, ReadResourceResult
    )
    from mcp.server.stdio import stdio_server
except ImportError as e:
    logging.error(f"MCP 패키지를 찾을 수 없습니다: {e}")
    logging.error("pip install mcp를 실행해주세요")
    sys.exit(1)

# A2A 시스템 imports
try:
    from config_secure import SecureConfig
    from skills import SkillManager
    from agent_card import A2AAgentCard
except ImportError as e:
    logging.error(f"A2A 시스템 모듈을 찾을 수 없습니다: {e}")
    # 개발 환경에서는 계속 진행
    SecureConfig = None
    SkillManager = None
    A2AAgentCard = None

# 로깅 설정
if SecureConfig:
    logger = SecureConfig.setup_logging()
else:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class A2AMCPServer:
    """A2A Agent System MCP Server"""
    
    def __init__(self):
        self.server = Server("a2a-agent-system")
        self.skill_manager = None
        self.agent_card = None
        self.config = SecureConfig if SecureConfig else None
        
        # 초기화
        self._initialize_components()
        self._setup_handlers()
    
    def _initialize_components(self):
        """A2A 시스템 구성요소 초기화"""
        try:
            if SkillManager:
                self.skill_manager = SkillManager()
                logger.info("스킬 매니저 초기화 완료")
            
            if A2AAgentCard:
                self.agent_card = A2AAgentCard()
                logger.info("A2A 에이전트 카드 초기화 완료")
                
        except Exception as e:
            logger.error(f"구성요소 초기화 오류: {e}")
            # 기본 구성으로 계속 진행
    
    def _setup_handlers(self):
        """MCP 서버 핸들러 설정"""
        
        @self.server.list_resources()
        async def handle_list_resources() -> ListResourcesResult:
            """사용 가능한 리소스 목록 반환"""
            resources = [
                Resource(
                    uri="agent://card",
                    name="A2A Agent Card",
                    description="A2A 에이전트 메타데이터 및 기능 정보",
                    mimeType="application/json"
                ),
                Resource(
                    uri="agent://status",
                    name="Server Status", 
                    description="서버 상태 및 사용 가능한 기능",
                    mimeType="application/json"
                ),
                Resource(
                    uri="agent://config",
                    name="Configuration",
                    description="서버 설정 정보 (민감한 정보 제외)",
                    mimeType="application/json"
                )
            ]
            
            return ListResourcesResult(resources=resources)
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> ReadResourceResult:
            """리소스 내용 읽기"""
            try:
                if uri == "agent://card":
                    if self.agent_card:
                        card_data = self.agent_card.generate_card()
                    else:
                        card_data = {
                            "name": "A2A-MCP-Agent",
                            "version": "1.0.0",
                            "description": "A2A compatible AI agent with MCP support",
                            "protocol": "a2a",
                            "protocol_version": "0.2.1"
                        }
                    
                    return ReadResourceResult(
                        contents=[
                            TextContent(
                                type="text",
                                text=json.dumps(card_data, indent=2, ensure_ascii=False)
                            )
                        ]
                    )
                
                elif uri == "agent://status":
                    if self.config:
                        validation = self.config.validate_deployment_readiness()
                        capabilities = self.config.get_available_capabilities()
                    else:
                        validation = {"status": "limited", "warnings": ["Config not available"]}
                        capabilities = {"tools": [], "resources": []}
                    
                    status_data = {
                        "server_status": "running",
                        "deployment_readiness": validation,
                        "available_capabilities": capabilities,
                        "mcp_version": "2024-11-05",
                        "a2a_compatible": True
                    }
                    
                    return ReadResourceResult(
                        contents=[
                            TextContent(
                                type="text", 
                                text=json.dumps(status_data, indent=2, ensure_ascii=False)
                            )
                        ]
                    )
                
                elif uri == "agent://config":
                    if self.config:
                        config_data = self.config.get_sanitized_config()
                    else:
                        config_data = {
                            "agent_name": "A2A-MCP-Agent",
                            "mcp_mode": "server",
                            "deployment_env": "development"
                        }
                    
                    return ReadResourceResult(
                        contents=[
                            TextContent(
                                type="text",
                                text=json.dumps(config_data, indent=2, ensure_ascii=False)
                            )
                        ]
                    )
                
                else:
                    raise ValueError(f"알 수 없는 리소스 URI: {uri}")
                    
            except Exception as e:
                logger.error(f"리소스 읽기 오류 {uri}: {e}")
                return ReadResourceResult(
                    contents=[
                        TextContent(
                            type="text",
                            text=f"오류: {str(e)}"
                        )
                    ]
                )
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """사용 가능한 도구 목록 반환"""
            tools = []
            
            # 기본 도구들
            if self.skill_manager:
                # 스킬 매니저가 있는 경우 실제 스킬들을 등록
                if hasattr(self.skill_manager, 'available_skills'):
                    for skill_name, skill_info in self.skill_manager.available_skills.items():
                        tools.append(
                            Tool(
                                name=skill_name,
                                description=skill_info.get('description', f'{skill_name} 기능'),
                                inputSchema={
                                    "type": "object",
                                    "properties": skill_info.get('parameters', {}),
                                    "required": skill_info.get('required', [])
                                }
                            )
                        )
            else:
                # 기본 도구들 정의
                tools = [
                    Tool(
                        name="generate_text",
                        description="AI 모델을 사용하여 텍스트 생성",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "prompt": {
                                    "type": "string",
                                    "description": "생성할 텍스트의 프롬프트"
                                },
                                "max_tokens": {
                                    "type": "integer", 
                                    "description": "최대 토큰 수",
                                    "default": 500
                                }
                            },
                            "required": ["prompt"]
                        }
                    ),
                    Tool(
                        name="analyze_text",
                        description="텍스트 분석 (감정, 요약, 인사이트)",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "text": {
                                    "type": "string",
                                    "description": "분석할 텍스트"
                                },
                                "analysis_type": {
                                    "type": "string",
                                    "enum": ["sentiment", "summary", "insights"],
                                    "description": "분석 유형",
                                    "default": "summary"
                                }
                            },
                            "required": ["text"]
                        }
                    ),
                    Tool(
                        name="web_search",
                        description="웹 검색 수행",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "검색 쿼리"
                                },
                                "max_results": {
                                    "type": "integer",
                                    "description": "최대 결과 수",
                                    "default": 5
                                }
                            },
                            "required": ["query"]
                        }
                    )
                ]
            
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
            """도구 실행"""
            try:
                logger.info(f"도구 호출: {name}, 인수: {arguments}")
                
                if self.skill_manager and hasattr(self.skill_manager, 'execute_skill'):
                    # 실제 스킬 매니저 사용
                    result = await self.skill_manager.execute_skill(name, arguments)
                else:
                    # 기본 구현 (데모용)
                    result = await self._execute_basic_tool(name, arguments)
                
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=str(result)
                        )
                    ]
                )
                
            except Exception as e:
                logger.error(f"도구 실행 오류 {name}: {e}")
                logger.error(traceback.format_exc())
                
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text", 
                            text=f"오류: {str(e)}"
                        )
                    ],
                    isError=True
                )
    
    async def _execute_basic_tool(self, name: str, arguments: dict) -> str:
        """기본 도구 구현 (스킬 매니저가 없는 경우)"""
        if name == "generate_text":
            prompt = arguments.get("prompt", "")
            return f"[Demo] 텍스트 생성 결과: '{prompt}'에 대한 AI 응답입니다."
        
        elif name == "analyze_text":
            text = arguments.get("text", "")
            analysis_type = arguments.get("analysis_type", "summary")
            return f"[Demo] {analysis_type} 분석 결과: '{text[:100]}...'에 대한 분석입니다."
        
        elif name == "web_search":
            query = arguments.get("query", "")
            max_results = arguments.get("max_results", 5)
            return f"[Demo] 웹 검색 결과: '{query}'에 대한 {max_results}개의 검색 결과입니다."
        
        else:
            raise ValueError(f"알 수 없는 도구: {name}")

async def main():
    """MCP 서버 메인 함수"""
    try:
        logger.info("A2A MCP 서버 시작 중...")
        
        # A2A MCP 서버 초기화
        a2a_server = A2AMCPServer()
        
        # 배포 준비 상태 확인
        if a2a_server.config:
            validation = a2a_server.config.validate_deployment_readiness()
            logger.info(f"배포 준비 상태: {validation['status']}")
            if validation.get('warnings'):
                for warning in validation['warnings']:
                    logger.warning(warning)
        
        # STDIO 서버 실행
        logger.info("MCP STDIO 서버 시작...")
        async with stdio_server() as (read_stream, write_stream):
            await a2a_server.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="a2a-agent-system",
                    server_version="1.0.0",
                    capabilities=a2a_server.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )
            
    except KeyboardInterrupt:
        logger.info("서버 종료 중...")
    except Exception as e:
        logger.error(f"서버 오류: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    # Smithery 배포 환경에서는 asyncio.run 사용
    asyncio.run(main()) 
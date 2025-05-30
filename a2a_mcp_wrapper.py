#!/usr/bin/env python3
"""
A2A MCP Wrapper
다른 프로젝트에서 A2A 에이전트 시스템을 쉽게 사용할 수 있는 래퍼
"""

import asyncio
import json
import os
from typing import Dict, Any, List, Optional, Union
from contextlib import asynccontextmanager

from mcp_client import MCPClient

class A2AAgent:
    """A2A 에이전트 시스템 래퍼 클래스"""
    
    def __init__(self, server_command: str = None):
        """
        A2A 에이전트 초기화
        
        Args:
            server_command: MCP 서버 실행 명령어 (선택사항)
        """
        self.client = MCPClient(server_command)
        self._connected = False
    
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        await self.disconnect()
    
    async def connect(self) -> bool:
        """에이전트 연결"""
        if not self._connected:
            self._connected = await self.client.connect()
        return self._connected
    
    async def disconnect(self):
        """에이전트 연결 해제"""
        if self._connected:
            await self.client.disconnect()
            self._connected = False
    
    async def is_alive(self) -> bool:
        """에이전트 생존 상태 확인"""
        try:
            if not self._connected:
                return False
            
            result = await self.client.ping()
            return result.get("status") == "pong"
        except:
            return False
    
    # === AI 기능 ===
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """
        텍스트 생성
        
        Args:
            prompt: 생성할 텍스트에 대한 프롬프트
            **kwargs: 추가 옵션 (model, max_tokens, temperature)
        
        Returns:
            생성된 텍스트
        """
        if not self._connected:
            raise RuntimeError("에이전트가 연결되지 않음")
        
        return await self.client.generate_text(prompt, **kwargs)
    
    async def analyze(self, text: str, analysis_type: str = "summary") -> Dict[str, Any]:
        """
        텍스트 분석
        
        Args:
            text: 분석할 텍스트
            analysis_type: 분석 유형 (summary, sentiment, keywords)
        
        Returns:
            분석 결과
        """
        if not self._connected:
            raise RuntimeError("에이전트가 연결되지 않음")
        
        return await self.client.analyze_text(text, analysis_type)
    
    async def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        웹 검색
        
        Args:
            query: 검색 쿼리
            num_results: 반환할 결과 수
        
        Returns:
            검색 결과 목록
        """
        if not self._connected:
            raise RuntimeError("에이전트가 연결되지 않음")
        
        return await self.client.web_search(query, num_results)
    
    async def weather(self, city: str) -> Dict[str, Any]:
        """
        날씨 정보 가져오기
        
        Args:
            city: 도시 이름
        
        Returns:
            날씨 정보
        """
        if not self._connected:
            raise RuntimeError("에이전트가 연결되지 않음")
        
        return await self.client.get_weather(city)
    
    # === 고급 기능 ===
    
    async def get_capabilities(self) -> List[Dict[str, Any]]:
        """사용 가능한 기능 목록"""
        if not self._connected:
            raise RuntimeError("에이전트가 연결되지 않음")
        
        return await self.client.list_tools()
    
    async def get_status(self) -> Dict[str, Any]:
        """에이전트 상태 정보"""
        if not self._connected:
            raise RuntimeError("에이전트가 연결되지 않음")
        
        status_json = await self.client.read_resource("agent://status")
        return json.loads(status_json)
    
    async def get_config(self) -> Dict[str, Any]:
        """에이전트 설정 정보"""
        if not self._connected:
            raise RuntimeError("에이전트가 연결되지 않음")
        
        config_json = await self.client.read_resource("agent://config")
        return json.loads(config_json)
    
    async def get_agent_card(self) -> Dict[str, Any]:
        """에이전트 카드 정보"""
        if not self._connected:
            raise RuntimeError("에이전트가 연결되지 않음")
        
        card_json = await self.client.read_resource("agent://card")
        return json.loads(card_json)


# === 편의 함수들 ===

@asynccontextmanager
async def a2a_agent(server_command: str = None):
    """
    A2A 에이전트 컨텍스트 매니저
    
    사용 예시:
        async with a2a_agent() as agent:
            result = await agent.generate("안녕하세요!")
            print(result)
    """
    agent = A2AAgent(server_command)
    try:
        await agent.connect()
        yield agent
    finally:
        await agent.disconnect()


async def quick_generate(prompt: str, **kwargs) -> str:
    """
    빠른 텍스트 생성 (일회성)
    
    Args:
        prompt: 생성할 텍스트에 대한 프롬프트
        **kwargs: 추가 옵션
    
    Returns:
        생성된 텍스트
    """
    async with a2a_agent() as agent:
        return await agent.generate(prompt, **kwargs)


async def quick_analyze(text: str, analysis_type: str = "summary") -> Dict[str, Any]:
    """
    빠른 텍스트 분석 (일회성)
    
    Args:
        text: 분석할 텍스트
        analysis_type: 분석 유형
    
    Returns:
        분석 결과
    """
    async with a2a_agent() as agent:
        return await agent.analyze(text, analysis_type)


async def quick_search(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    빠른 웹 검색 (일회성)
    
    Args:
        query: 검색 쿼리
        num_results: 반환할 결과 수
    
    Returns:
        검색 결과
    """
    async with a2a_agent() as agent:
        return await agent.search(query, num_results)


# === 동기 버전 (편의용) ===

def sync_generate(prompt: str, **kwargs) -> str:
    """동기 버전 텍스트 생성"""
    return asyncio.run(quick_generate(prompt, **kwargs))


def sync_analyze(text: str, analysis_type: str = "summary") -> Dict[str, Any]:
    """동기 버전 텍스트 분석"""
    return asyncio.run(quick_analyze(text, analysis_type))


def sync_search(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """동기 버전 웹 검색"""
    return asyncio.run(quick_search(query, num_results))


# === 사용 예시 ===

async def example_usage():
    """사용 예시"""
    print("🚀 A2A 에이전트 래퍼 사용 예시\n")
    
    # 방법 1: 컨텍스트 매니저 사용
    print("📝 방법 1: 컨텍스트 매니저")
    async with a2a_agent() as agent:
        result = await agent.generate("파이썬의 장점을 3가지 말해주세요.")
        print(f"결과: {result[:100]}...\n")
    
    # 방법 2: 직접 연결 관리
    print("🔧 방법 2: 직접 연결 관리")
    agent = A2AAgent()
    try:
        await agent.connect()
        
        # 여러 작업 수행
        status = await agent.get_status()
        print(f"서버 상태: {status['server']}")
        
        capabilities = await agent.get_capabilities()
        print(f"사용 가능한 기능: {len(capabilities)}개")
        
        analysis = await agent.analyze("Python is a great programming language.")
        print(f"분석 결과: {analysis}")
        
    finally:
        await agent.disconnect()
    
    # 방법 3: 편의 함수 사용
    print("\n⚡ 방법 3: 편의 함수")
    result = await quick_generate("간단한 인사말을 만들어주세요.")
    print(f"빠른 생성: {result}")
    
    # 방법 4: 동기 버전 (주의: 비효율적)
    print("\n🔄 방법 4: 동기 버전")
    sync_result = sync_generate("짧은 농담을 말해주세요.")
    print(f"동기 결과: {sync_result}")


if __name__ == "__main__":
    asyncio.run(example_usage()) 
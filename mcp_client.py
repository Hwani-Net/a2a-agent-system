#!/usr/bin/env python3
"""
A2A Agent System MCP Client
다른 프로젝트에서 A2A 에이전트 시스템을 호출하기 위한 클라이언트
"""

import json
import asyncio
import subprocess
import logging
from typing import Dict, Any, List, Optional
import uuid
import os
import sys

class MCPClient:
    """A2A MCP 서버 클라이언트"""
    
    def __init__(self, server_command: str = None):
        """
        MCP 클라이언트 초기화
        
        Args:
            server_command: MCP 서버 실행 명령어
        """
        self.server_command = server_command or self._get_default_server_command()
        self.process = None
        self.initialized = False
        
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """로깅 설정"""
        logger = logging.getLogger("a2a_mcp_client")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _get_default_server_command(self) -> str:
        """기본 서버 명령어 반환"""
        # 현재 스크립트와 같은 디렉토리의 mcp_server.py 실행
        script_dir = os.path.dirname(os.path.abspath(__file__))
        server_path = os.path.join(script_dir, "mcp_server.py")
        
        return f"python {server_path}"
    
    async def connect(self) -> bool:
        """MCP 서버에 연결"""
        try:
            # 서버 프로세스 시작
            self.process = subprocess.Popen(
                self.server_command.split(),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0
            )
            
            # 서버 초기화
            init_response = await self._send_request("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {
                        "listChanged": True
                    },
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "a2a-client",
                    "version": "1.0.0"
                }
            })
            
            if "result" in init_response:
                self.initialized = True
                self.logger.info("MCP 서버 연결 완료")
                
                # 초기화 완료 알림
                await self._send_notification("notifications/initialized", {})
                
                return True
            else:
                self.logger.error(f"서버 초기화 실패: {init_response}")
                return False
                
        except Exception as e:
            self.logger.error(f"서버 연결 실패: {e}")
            return False
    
    async def disconnect(self):
        """서버 연결 해제"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            
            self.process = None
            self.initialized = False
            self.logger.info("MCP 서버 연결 해제")
    
    async def _send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """서버에 요청 전송"""
        if not self.process:
            raise RuntimeError("서버에 연결되지 않음")
        
        request_id = str(uuid.uuid4())
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params or {}
        }
        
        try:
            # 요청 전송
            request_json = json.dumps(request, ensure_ascii=False) + "\n"
            self.process.stdin.write(request_json)
            self.process.stdin.flush()
            
            # 응답 받기
            response_line = self.process.stdout.readline()
            if not response_line:
                raise RuntimeError("서버로부터 응답 없음")
            
            response = json.loads(response_line.strip())
            return response
            
        except Exception as e:
            self.logger.error(f"요청 전송 오류: {e}")
            raise
    
    async def _send_notification(self, method: str, params: Dict[str, Any] = None):
        """서버에 알림 전송 (응답 없음)"""
        if not self.process:
            raise RuntimeError("서버에 연결되지 않음")
        
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {}
        }
        
        try:
            notification_json = json.dumps(notification, ensure_ascii=False) + "\n"
            self.process.stdin.write(notification_json)
            self.process.stdin.flush()
            
        except Exception as e:
            self.logger.error(f"알림 전송 오류: {e}")
            raise
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """사용 가능한 도구 목록 가져오기"""
        if not self.initialized:
            raise RuntimeError("서버가 초기화되지 않음")
        
        response = await self._send_request("tools/list")
        if "result" in response:
            return response["result"]["tools"]
        else:
            raise RuntimeError(f"도구 목록 가져오기 실패: {response}")
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """도구 호출"""
        if not self.initialized:
            raise RuntimeError("서버가 초기화되지 않음")
        
        response = await self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        
        if "result" in response:
            return response["result"]
        else:
            raise RuntimeError(f"도구 호출 실패: {response}")
    
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """텍스트 생성"""
        arguments = {"prompt": prompt}
        arguments.update(kwargs)
        
        result = await self.call_tool("generate_text", arguments)
        
        # 결과 파싱
        if "content" in result and result["content"]:
            content_text = result["content"][0]["text"]
            try:
                parsed_result = json.loads(content_text)
                return parsed_result.get("content", content_text)
            except json.JSONDecodeError:
                return content_text
        else:
            return ""
    
    async def analyze_text(self, text: str, analysis_type: str = "summary") -> Dict[str, Any]:
        """텍스트 분석"""
        result = await self.call_tool("analyze_text", {
            "text": text,
            "analysis_type": analysis_type
        })
        
        if "content" in result and result["content"]:
            content_text = result["content"][0]["text"]
            try:
                return json.loads(content_text)
            except json.JSONDecodeError:
                return {"analysis": content_text}
        else:
            return {}
    
    async def web_search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """웹 검색"""
        result = await self.call_tool("web_search", {
            "query": query,
            "num_results": num_results
        })
        
        if "content" in result and result["content"]:
            content_text = result["content"][0]["text"]
            try:
                parsed_result = json.loads(content_text)
                return parsed_result.get("results", [])
            except json.JSONDecodeError:
                return []
        else:
            return []
    
    async def get_weather(self, city: str) -> Dict[str, Any]:
        """날씨 정보 가져오기"""
        result = await self.call_tool("get_weather", {
            "city": city
        })
        
        if "content" in result and result["content"]:
            content_text = result["content"][0]["text"]
            try:
                return json.loads(content_text)
            except json.JSONDecodeError:
                return {"weather": content_text}
        else:
            return {}
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """사용 가능한 리소스 목록"""
        response = await self._send_request("resources/list")
        if "result" in response:
            return response["result"]["resources"]
        else:
            raise RuntimeError(f"리소스 목록 가져오기 실패: {response}")
    
    async def read_resource(self, uri: str) -> str:
        """리소스 읽기"""
        response = await self._send_request("resources/read", {"uri": uri})
        if "result" in response:
            contents = response["result"]["contents"]
            if contents:
                return contents[0]["text"]
        
        raise RuntimeError(f"리소스 읽기 실패: {response}")
    
    async def list_prompts(self) -> List[Dict[str, Any]]:
        """사용 가능한 프롬프트 목록"""
        response = await self._send_request("prompts/list")
        if "result" in response:
            return response["result"]["prompts"]
        else:
            raise RuntimeError(f"프롬프트 목록 가져오기 실패: {response}")
    
    async def get_prompt(self, name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """프롬프트 가져오기"""
        response = await self._send_request("prompts/get", {
            "name": name,
            "arguments": arguments or {}
        })
        
        if "result" in response:
            return response["result"]
        else:
            raise RuntimeError(f"프롬프트 가져오기 실패: {response}")
    
    async def ping(self) -> Dict[str, Any]:
        """서버 상태 확인"""
        response = await self._send_request("ping")
        if "result" in response:
            return response["result"]
        else:
            raise RuntimeError(f"핑 실패: {response}")

# 사용 예시
async def example_usage():
    """사용 예시"""
    client = MCPClient()
    
    try:
        # 서버 연결
        if await client.connect():
            print("✅ MCP 서버 연결 성공")
            
            # 도구 목록 확인
            tools = await client.list_tools()
            print(f"\n📋 사용 가능한 도구: {len(tools)}개")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
            
            # 텍스트 생성 예시
            print("\n🤖 텍스트 생성 테스트:")
            text = await client.generate_text("파이썬에 대한 간단한 설명을 써주세요.")
            print(f"결과: {text[:100]}...")
            
            # 텍스트 분석 예시
            print("\n📊 텍스트 분석 테스트:")
            analysis = await client.analyze_text("파이썬은 간단하고 읽기 쉬운 프로그래밍 언어입니다.")
            print(f"분석 결과: {analysis}")
            
            # 서버 상태 확인
            ping_result = await client.ping()
            print(f"\n💓 서버 상태: {ping_result}")
            
        else:
            print("❌ MCP 서버 연결 실패")
    
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    finally:
        # 연결 해제
        await client.disconnect()
        print("\n🔌 서버 연결 해제")

if __name__ == "__main__":
    asyncio.run(example_usage()) 
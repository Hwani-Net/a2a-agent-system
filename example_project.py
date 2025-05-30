#!/usr/bin/env python3
"""
Example Project Using A2A Agent System
다른 프로젝트에서 A2A 에이전트 시스템을 사용하는 예시
"""

import asyncio
import json
from datetime import datetime

# A2A 에이전트 시스템 import (실제 사용 시)
# from a2a_agent_system import a2a_agent, quick_generate, A2AAgent

# 현재 디렉토리에서 테스트용 (개발 중)
from a2a_mcp_wrapper import a2a_agent, quick_generate, A2AAgent


class MyProjectApp:
    """A2A 에이전트를 사용하는 예시 애플리케이션"""
    
    def __init__(self):
        self.name = "My AI-Powered Project"
        self.version = "1.0.0"
        self.agent = None
    
    async def initialize(self):
        """애플리케이션 초기화"""
        print(f"🚀 {self.name} v{self.version} 시작")
        print("🔗 A2A 에이전트 연결 중...")
        
        self.agent = A2AAgent()
        success = await self.agent.connect()
        
        if success:
            print("✅ A2A 에이전트 연결 성공")
            return True
        else:
            print("❌ A2A 에이전트 연결 실패")
            return False
    
    async def cleanup(self):
        """애플리케이션 정리"""
        if self.agent:
            await self.agent.disconnect()
            print("🔌 A2A 에이전트 연결 해제")
    
    async def show_capabilities(self):
        """사용 가능한 기능 표시"""
        print("\n📋 사용 가능한 AI 기능:")
        
        try:
            capabilities = await self.agent.get_capabilities()
            for i, cap in enumerate(capabilities, 1):
                print(f"  {i}. {cap['name']}: {cap['description']}")
        except Exception as e:
            print(f"❌ 기능 목록 조회 실패: {e}")
    
    async def content_generator(self):
        """콘텐츠 생성 기능"""
        print("\n📝 콘텐츠 생성 예시")
        
        try:
            # 블로그 포스트 생성
            prompt = """
            다음 주제로 블로그 포스트를 작성해주세요:
            - 주제: 'AI와 소프트웨어 개발의 미래'
            - 길이: 약 300단어
            - 톤: 전문적이지만 친근한
            """
            
            print("🤖 AI가 블로그 포스트를 생성 중...")
            blog_post = await self.agent.generate(prompt, max_tokens=400)
            
            print("✅ 생성 완료:")
            print("-" * 50)
            print(blog_post)
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ 콘텐츠 생성 실패: {e}")
    
    async def text_analyzer(self):
        """텍스트 분석 기능"""
        print("\n📊 텍스트 분석 예시")
        
        sample_text = """
        인공지능 기술의 발전으로 소프트웨어 개발 방식이 크게 변화하고 있습니다. 
        코드 자동 생성, 버그 탐지, 성능 최적화 등 다양한 영역에서 AI가 활용되고 있으며, 
        개발자들의 생산성이 향상되고 있습니다. 하지만 동시에 새로운 도전과제들도 등장하고 있어 
        개발자들은 지속적인 학습과 적응이 필요한 상황입니다.
        """
        
        try:
            print("🔍 텍스트 분석 중...")
            
            # 요약 분석
            summary = await self.agent.analyze(sample_text, "summary")
            print(f"📄 요약: {summary}")
            
            # 감정 분석
            sentiment = await self.agent.analyze(sample_text, "sentiment")
            print(f"😊 감정: {sentiment}")
            
        except Exception as e:
            print(f"❌ 텍스트 분석 실패: {e}")
    
    async def research_assistant(self):
        """리서치 어시스턴트 기능"""
        print("\n🔍 리서치 어시스턴트 예시")
        
        try:
            # 웹 검색
            query = "2024 AI 개발 트렌드"
            print(f"🌐 '{query}' 검색 중...")
            
            search_results = await self.agent.search(query, num_results=3)
            
            print("✅ 검색 결과:")
            for i, result in enumerate(search_results, 1):
                print(f"  {i}. {result.get('title', 'No title')}")
                print(f"     URL: {result.get('url', 'No URL')}")
                print(f"     설명: {result.get('description', 'No description')[:100]}...")
                print()
            
        except Exception as e:
            print(f"❌ 웹 검색 실패: {e}")
    
    async def weather_service(self):
        """날씨 서비스 기능"""
        print("\n🌤️ 날씨 서비스 예시")
        
        try:
            city = "Seoul"
            print(f"🌍 {city}의 날씨 정보 조회 중...")
            
            weather = await self.agent.weather(city)
            print(f"✅ 날씨 정보: {weather}")
            
        except Exception as e:
            print(f"❌ 날씨 조회 실패: {e}")
    
    async def health_check(self):
        """에이전트 상태 확인"""
        print("\n💓 에이전트 상태 확인")
        
        try:
            # 생존 확인
            is_alive = await self.agent.is_alive()
            print(f"🔄 에이전트 생존: {'✅ 정상' if is_alive else '❌ 비정상'}")
            
            # 상태 정보
            status = await self.agent.get_status()
            print(f"⚙️ 서버 상태: {status.get('server', 'Unknown')}")
            print(f"📊 활성 세션: {status.get('active_sessions', 0)}개")
            
            # 설정 정보
            config = await self.agent.get_config()
            print(f"🤖 사용 가능한 모델: {config.get('available_models', [])}")
            
        except Exception as e:
            print(f"❌ 상태 확인 실패: {e}")
    
    async def run_all_examples(self):
        """모든 예시 실행"""
        examples = [
            ("기능 목록 확인", self.show_capabilities),
            ("콘텐츠 생성", self.content_generator),
            ("텍스트 분석", self.text_analyzer),
            ("리서치 어시스턴트", self.research_assistant),
            ("날씨 서비스", self.weather_service),
            ("상태 확인", self.health_check)
        ]
        
        print(f"\n🎯 {len(examples)}개의 예시를 실행합니다...\n")
        
        for name, func in examples:
            print(f"\n{'='*60}")
            print(f"🔥 {name}")
            print(f"{'='*60}")
            
            try:
                await func()
            except Exception as e:
                print(f"❌ {name} 실행 중 오류: {e}")
            
            # 잠시 대기
            await asyncio.sleep(1)
        
        print(f"\n{'='*60}")
        print("🎉 모든 예시 실행 완료!")
        print(f"{'='*60}")


async def quick_examples():
    """편의 함수들을 사용한 빠른 예시"""
    print("\n⚡ 편의 함수 사용 예시")
    print("="*40)
    
    try:
        # 빠른 텍스트 생성
        print("🚀 빠른 텍스트 생성:")
        result = await quick_generate("Python의 장점 3가지를 간단히 설명해주세요.")
        print(f"📝 결과: {result[:200]}...")
        
        # 컨텍스트 매니저 사용
        print("\n🔧 컨텍스트 매니저 사용:")
        async with a2a_agent() as agent:
            greeting = await agent.generate("친근한 인사말을 만들어주세요.")
            print(f"👋 인사말: {greeting}")
            
            analysis = await agent.analyze("이것은 테스트 문장입니다.", "summary")
            print(f"📊 분석: {analysis}")
        
    except Exception as e:
        print(f"❌ 편의 함수 예시 실패: {e}")


async def main():
    """메인 함수"""
    print("🌟 A2A Agent System 사용 예시 프로젝트")
    print("="*50)
    
    # 1. 편의 함수 예시
    await quick_examples()
    
    # 2. 완전한 애플리케이션 예시
    app = MyProjectApp()
    
    try:
        # 초기화
        if await app.initialize():
            # 모든 예시 실행
            await app.run_all_examples()
        else:
            print("❌ 애플리케이션 초기화 실패")
    
    except KeyboardInterrupt:
        print("\n⏹️ 사용자가 중단했습니다.")
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
    finally:
        # 정리
        await app.cleanup()
        print("\n👋 예시 프로젝트 종료")


if __name__ == "__main__":
    asyncio.run(main()) 
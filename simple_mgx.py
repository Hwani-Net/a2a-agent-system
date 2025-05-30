#!/usr/bin/env python3
"""
Cursor에서 한 줄 명령으로 MGX 팀 기능을 사용할 수 있는 간단한 도구
예: python simple_mgx.py "React 로그인 컴포넌트 만들어줘"
"""
import asyncio
import sys
from mgx_inspired_agent_team import MGXAgentTeam
from datetime import datetime

class SimpleMGX:
    def __init__(self):
        self.mgx_team = MGXAgentTeam()
    
    async def quick_action(self, user_request: str):
        """사용자 요청을 분석하고 적절한 MGX 액션 실행"""
        print(f"🚀 MGX 팀이 '{user_request}' 요청을 처리합니다...\n")
        
        # 간단한 키워드 분석
        request_lower = user_request.lower()
        
        try:
            if any(word in request_lower for word in ['프로젝트', 'project', '만들어', 'create']):
                await self.create_and_work_on_project(user_request)
            elif any(word in request_lower for word in ['코드', 'code', '컴포넌트', '함수', '클래스']):
                await self.generate_code_directly(user_request)
            elif any(word in request_lower for word in ['토론', 'discuss', '의견', '생각']):
                await self.quick_discussion(user_request)
            elif any(word in request_lower for word in ['팀', 'team', '소개', '누구']):
                await self.show_team_info()
            else:
                # 기본적으로 코드 생성으로 처리
                await self.generate_code_directly(user_request)
        
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
    
    async def show_team_info(self):
        """팀 정보 표시"""
        print("👥 MGX AI 개발팀:")
        team_info = await self.mgx_team.get_team_info()
        
        for member in team_info['members']:
            status = "🟢" if member['status'] == 'available' else "🔴"
            print(f"  {status} {member['name']} - {member['role']}")
            print(f"     {member['expertise']}")
    
    async def create_and_work_on_project(self, request: str):
        """프로젝트 생성 및 작업"""
        project_name = f"사용자 요청 프로젝트 - {datetime.now().strftime('%H:%M')}"
        
        print(f"🎯 프로젝트 '{project_name}' 생성 중...")
        project = await self.mgx_team.create_project(
            name=project_name,
            description=request,
            requirements=[request]
        )
        
        print(f"✅ 프로젝트 생성 완료!")
        print(f"   📋 ID: {project['project_id']}")
        print(f"   👥 담당팀: {', '.join(project['team_assignments'])}")
        
        # 바로 코드 생성도 진행
        print(f"\n⚡ Alex가 코드를 생성합니다...")
        artifact = await self.mgx_team.generate_artifact(
            project_id=project['project_id'],
            artifact_type="code",
            description=request,
            assigned_agent="Alex"
        )
        
        print(f"\n💻 생성된 코드:")
        print(f"  📁 파일: {artifact['metadata'].get('filename', 'code.txt')}")
        print(f"  📏 크기: {len(artifact['content'])} 문자")
        print(f"  👨‍💻 작성자: {artifact['created_by']}")
        print("\n" + "="*50)
        print(artifact['content'])
        print("="*50)
    
    async def generate_code_directly(self, request: str):
        """빠른 코드 생성"""
        # 임시 프로젝트 생성
        temp_project = await self.mgx_team.create_project(
            name=f"빠른작업-{datetime.now().strftime('%H%M%S')}",
            description="빠른 코드 생성",
            requirements=[request]
        )
        
        print(f"⚡ Alex가 '{request}' 코드를 생성합니다...")
        artifact = await self.mgx_team.generate_artifact(
            project_id=temp_project['project_id'],
            artifact_type="code",
            description=request,
            assigned_agent="Alex"
        )
        
        print(f"\n💻 생성된 코드:")
        print(f"  📁 파일: {artifact['metadata'].get('filename', 'generated.txt')}")
        print(f"  🔧 언어: {artifact['metadata'].get('language', '감지됨')}")
        print(f"  📏 크기: {len(artifact['content'])} 문자")
        print("\n" + "="*50)
        print(artifact['content'])
        print("="*50)
        
        # 사용 팁
        print(f"\n💡 팁: 이 코드를 파일로 저장하려면:")
        filename = artifact['metadata'].get('filename', 'generated_code.txt')
        print(f"   echo '{artifact['content'][:50]}...' > {filename}")
    
    async def quick_discussion(self, topic: str):
        """빠른 팀 토론"""
        # 임시 프로젝트로 토론 진행
        temp_project = await self.mgx_team.create_project(
            name=f"토론-{datetime.now().strftime('%H%M%S')}",
            description="팀 토론",
            requirements=[topic]
        )
        
        print(f"💬 '{topic}'에 대한 팀 토론을 시작합니다...")
        discussion = await self.mgx_team.start_team_discussion(
            project_id=temp_project['project_id'],
            topic=topic,
            participants=["Mike", "Emma", "Alex"]
        )
        
        print(f"\n🎯 토론 결과:")
        for comment in discussion['comments']:
            print(f"  💭 {comment['author']}: {comment['content']}")
        
        if discussion['decisions']:
            print(f"\n📋 팀 결정사항:")
            for decision in discussion['decisions']:
                print(f"  ✅ {decision}")

def main():
    if len(sys.argv) < 2:
        print("사용법:")
        print("  python simple_mgx.py \"요청 내용\"")
        print("\n예시:")
        print("  python simple_mgx.py \"React 로그인 컴포넌트 만들어줘\"")
        print("  python simple_mgx.py \"FastAPI REST API 만들어줘\"")
        print("  python simple_mgx.py \"팀 소개해줘\"")
        print("  python simple_mgx.py \"데이터베이스 설계에 대해 토론해줘\"")
        return
    
    user_request = " ".join(sys.argv[1:])
    mgx = SimpleMGX()
    asyncio.run(mgx.quick_action(user_request))

if __name__ == "__main__":
    main() 
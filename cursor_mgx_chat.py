#!/usr/bin/env python3
"""
Cursor에서 MGX 팀과 바로 대화할 수 있는 통합 인터페이스
서버를 따로 실행하지 않고도 MGX 기능을 사용할 수 있습니다.
"""
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from mgx_inspired_agent_team import MGXAgentTeam, TeamMember
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class CursorMGXInterface:
    """Cursor에서 MGX 팀과 직접 대화할 수 있는 인터페이스"""
    
    def __init__(self):
        self.mgx_team = MGXAgentTeam()
        self.current_project = None
        self.chat_history = []
        
    async def start_chat(self):
        """채팅 시작"""
        print("=" * 60)
        print("🚀 MGX AI 개발팀에 오신 것을 환영합니다!")
        print("=" * 60)
        
        # 팀원 소개
        await self.show_team()
        
        print("\n💡 사용 가능한 명령어:")
        print("  - 'team': 팀원 정보 보기")
        print("  - 'project <이름>': 새 프로젝트 생성")
        print("  - 'discuss <주제>': 팀 토론 시작")
        print("  - 'generate <설명>': 코드 생성")
        print("  - 'status': 현재 프로젝트 상태")
        print("  - 'history': 대화 내역")
        print("  - 'quit': 종료")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n🔮 당신: ").strip()
                
                if user_input.lower() == 'quit':
                    print("👋 MGX 팀과의 대화를 종료합니다. 좋은 하루 되세요!")
                    break
                    
                if user_input.lower() == 'team':
                    await self.show_team()
                    continue
                    
                if user_input.lower().startswith('project '):
                    project_name = user_input[8:].strip()
                    await self.create_project(project_name)
                    continue
                    
                if user_input.lower().startswith('discuss '):
                    topic = user_input[8:].strip()
                    await self.start_discussion(topic)
                    continue
                    
                if user_input.lower().startswith('generate '):
                    description = user_input[9:].strip()
                    await self.generate_code(description)
                    continue
                    
                if user_input.lower() == 'status':
                    await self.show_project_status()
                    continue
                    
                if user_input.lower() == 'history':
                    self.show_chat_history()
                    continue
                
                # 일반 대화
                await self.general_chat(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 MGX 팀과의 대화를 종료합니다.")
                break
            except Exception as e:
                print(f"❌ 오류가 발생했습니다: {e}")
    
    async def show_team(self):
        """팀원 정보 표시"""
        print("\n👥 MGX AI 개발팀:")
        team_info = await self.mgx_team.get_team_info()
        
        for member in team_info['members']:
            status = "🟢" if member['status'] == 'available' else "🔴"
            print(f"  {status} {member['name']} ({member['role']})")
            print(f"     💪 {member['expertise']}")
            print(f"     📝 {member['description']}")
            print()
    
    async def create_project(self, project_name: str):
        """새 프로젝트 생성"""
        print(f"\n🎯 프로젝트 '{project_name}' 생성 중...")
        
        try:
            result = await self.mgx_team.create_project(
                name=project_name,
                description=f"사용자가 요청한 프로젝트: {project_name}",
                requirements=["사용자 요구사항에 맞는 구현", "모던한 기술 스택 사용"]
            )
            
            self.current_project = result
            self.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'project_creation',
                'content': result
            })
            
            print(f"✅ 프로젝트가 생성되었습니다!")
            print(f"   📋 프로젝트 ID: {result['project_id']}")
            print(f"   👥 참여 팀원: {', '.join(result['team_assignments'])}")
            
        except Exception as e:
            print(f"❌ 프로젝트 생성 실패: {e}")
    
    async def start_discussion(self, topic: str):
        """팀 토론 시작"""
        print(f"\n💬 토론 주제: '{topic}'")
        print("팀원들이 의견을 나누고 있습니다...")
        
        try:
            if not self.current_project:
                print("⚠️  먼저 프로젝트를 생성해주세요. (예: project 웹사이트)")
                return
            
            result = await self.mgx_team.start_team_discussion(
                project_id=self.current_project['project_id'],
                topic=topic,
                participants=["Mike", "Alex", "Emma"]
            )
            
            self.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'discussion',
                'content': result
            })
            
            print(f"🎯 토론 결과:")
            for comment in result['comments']:
                print(f"  💭 {comment['author']}: {comment['content']}")
            
            if result['decisions']:
                print(f"\n📋 결정사항:")
                for decision in result['decisions']:
                    print(f"  ✅ {decision}")
            
        except Exception as e:
            print(f"❌ 토론 시작 실패: {e}")
    
    async def generate_code(self, description: str):
        """코드 생성"""
        print(f"\n⚡ 코드 생성 중: '{description}'")
        
        try:
            if not self.current_project:
                print("⚠️  먼저 프로젝트를 생성해주세요.")
                return
            
            result = await self.mgx_team.generate_artifact(
                project_id=self.current_project['project_id'],
                artifact_type="code",
                description=description,
                assigned_agent="Alex"
            )
            
            self.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'code_generation',
                'content': result
            })
            
            print(f"🎨 생성된 코드:")
            print(f"  📁 파일: {result['metadata'].get('filename', 'generated_code')}")
            print(f"  🔧 언어: {result['metadata'].get('language', 'unknown')}")
            print(f"  📏 크기: {len(result['content'])} 문자")
            print(f"  👨‍💻 작성자: {result['created_by']}")
            print()
            print("💻 코드 내용:")
            print("-" * 40)
            print(result['content'])
            print("-" * 40)
            
        except Exception as e:
            print(f"❌ 코드 생성 실패: {e}")
    
    async def show_project_status(self):
        """프로젝트 상태 표시"""
        if not self.current_project:
            print("⚠️  활성 프로젝트가 없습니다.")
            return
        
        try:
            status = await self.mgx_team.get_project_status(
                self.current_project['project_id']
            )
            
            print(f"\n📊 프로젝트 상태:")
            print(f"  📋 이름: {status['name']}")
            print(f"  🎯 상태: {status['status']}")
            print(f"  📈 진행률: {status['progress']}%")
            print(f"  👥 참여자: {', '.join(status['team_assignments'])}")
            print(f"  📅 생성일: {status['created_at']}")
            
            if status['artifacts']:
                print(f"  🎨 생성된 아티팩트: {len(status['artifacts'])}개")
                for artifact in status['artifacts'][:3]:  # 최근 3개만 표시
                    print(f"    - {artifact['artifact_id']}: {artifact['type']}")
            
        except Exception as e:
            print(f"❌ 상태 조회 실패: {e}")
    
    def show_chat_history(self):
        """채팅 내역 표시"""
        if not self.chat_history:
            print("📭 채팅 내역이 없습니다.")
            return
        
        print(f"\n📜 채팅 내역 (최근 5개):")
        for entry in self.chat_history[-5:]:
            timestamp = entry['timestamp'][:19].replace('T', ' ')
            type_emoji = {
                'project_creation': '🎯',
                'discussion': '💬',
                'code_generation': '⚡',
                'general_chat': '💭'
            }.get(entry['type'], '📝')
            
            print(f"  {type_emoji} {timestamp} - {entry['type']}")
    
    async def general_chat(self, message: str):
        """일반 대화"""
        print(f"\n💭 팀장 Mike가 응답합니다...")
        
        # 간단한 응답 로직 (실제로는 더 복잡한 AI 응답을 구현할 수 있음)
        responses = {
            "안녕": "안녕하세요! MGX 팀장 Mike입니다. 무엇을 도와드릴까요?",
            "도움": "저희 팀은 프로젝트 생성, 코드 개발, 팀 토론을 도와드립니다!",
            "기능": "project <이름>, discuss <주제>, generate <설명> 명령어를 사용해보세요!",
        }
        
        response = responses.get(message.lower(), 
                               f"'{message}'에 대해 팀과 논의해보겠습니다. 구체적인 요청이 있으시면 명령어를 사용해주세요!")
        
        print(f"🤖 Mike: {response}")
        
        self.chat_history.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'general_chat',
            'content': {'user': message, 'response': response}
        })

def main():
    """메인 함수"""
    print("🔧 MGX 팀 초기화 중...")
    interface = CursorMGXInterface()
    
    try:
        asyncio.run(interface.start_chat())
    except Exception as e:
        print(f"❌ 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main() 
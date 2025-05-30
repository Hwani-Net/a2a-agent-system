#!/usr/bin/env python3
"""
MGX 팀 협업 워크플로우 데모
Dream, Chat, Create - 실제 팀 협업 과정을 체험해보세요!
"""
import requests
import json
import time

class MGXWorkflowDemo:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def step(self, step_num, title, description=""):
        """단계별 표시"""
        print(f"\n{'='*60}")
        print(f"🎯 {step_num}단계: {title}")
        if description:
            print(f"💭 {description}")
        print(f"{'='*60}")
        time.sleep(1)
    
    def a2a_call(self, method, params=None):
        """A2A 프로토콜 호출"""
        payload = {
            "jsonrpc": "2.0", 
            "method": method,
            "id": f"demo_{int(time.time())}"
        }
        if params:
            payload["params"] = params
        
        try:
            response = self.session.post(f"{self.base_url}/a2a", json=payload)
            result = response.json()
            
            # 디버깅용 출력
            print(f"🔍 Debug - API Response: {result}")
            
            if "error" in result and result["error"] is not None:
                print(f"❌ Error: {result['error']}")
                return None
            
            if "result" in result:
                return result["result"]
            else:
                print(f"⚠️  No result field in response: {result}")
                return None
                
        except Exception as e:
            print(f"❌ Exception during API call: {e}")
            return None
    
    def show_team(self):
        """팀 소개"""
        self.step(1, "팀 소개", "우리의 24/7 AI 개발팀을 만나보세요")
        
        team_info = self.a2a_call("mgx/team_info")
        if team_info:
            print(f"🏢 {team_info['team_name']}")
            print(f"📝 {team_info['description']}")
            print(f"\n👥 팀 멤버들:")
            
            for member in team_info['members']:
                print(f"   {member['avatar']} {member['name']} ({member['role']})")
                print(f"      └─ {member['description']}")
                print(f"      └─ 전문분야: {', '.join(member['specialties'])}")
                print()
        
        input("📱 Press Enter to continue...")
    
    def create_project(self, project_description):
        """프로젝트 생성"""
        self.step(2, "프로젝트 생성", f"새로운 프로젝트를 시작합니다: {project_description}")
        
        result = self.a2a_call("mgx/create_project", {
            "description": project_description,
            "user_id": "demo_user"
        })
        
        if result:
            project_id = result["project_id"]
            print(f"✅ 프로젝트 생성 완료!")
            print(f"🆔 프로젝트 ID: {project_id[:8]}...")
            print(f"📊 상태: {result['status']}")
            print(f"💬 메시지: {result['message']}")
            
            input("📱 Press Enter to continue...")
            return project_id
        return None
    
    def team_discussion(self, project_id, topic):
        """팀 토론"""
        self.step(3, "팀 토론", f"주제: {topic}")
        
        print("🔄 팀 멤버들이 토론 중입니다...")
        time.sleep(2)
        
        result = self.a2a_call("mgx/team_discussion", {
            "project_id": project_id,
            "topic": topic
        })
        
        if result:
            print(f"💬 토론 완료! {result['participants']}명 참여")
            print(f"📋 주제: {result['topic']}")
            print("\n🗣️ 팀 멤버 의견:")
            
            for i, discussion in enumerate(result['discussion'], 1):
                agent = discussion['agent']
                avatar = discussion['avatar']
                contribution = discussion['contribution']
                
                print(f"\n{i}. {avatar} {agent}:")
                print(f"   {contribution}")
                
                if i < len(result['discussion']):
                    time.sleep(1)  # 실시간 느낌
            
            input("\n📱 Press Enter to continue...")
            return result
        return None
    
    def generate_artifact(self, project_id, component_type):
        """코드/아티팩트 생성"""
        self.step(4, "코드 생성", f"Alex가 {component_type}를 생성합니다")
        
        print("⚡ 코드 생성 중...")
        time.sleep(3)
        
        result = self.a2a_call("mgx/generate_artifact", {
            "project_id": project_id,
            "component_type": component_type
        })
        
        if result:
            artifact = result["artifact"]
            print(f"✅ {result['message']}")
            print(f"🆔 아티팩트 ID: {artifact['id'][:8]}...")
            print(f"📝 타입: {artifact['component_type']}")
            print(f"👨‍💻 작성자: {artifact['created_by']}")
            print(f"📅 생성일: {artifact['created_at']}")
            print(f"🔖 버전: {artifact['version']}")
            
            print(f"\n📋 생성된 코드 (처음 500자):")
            print("```")
            print(artifact['content'][:500])
            if len(artifact['content']) > 500:
                print("...")
            print("```")
            
            input("\n📱 Press Enter to continue...")
            return artifact
        return None
    
    def follow_up_discussion(self, project_id):
        """후속 토론"""
        self.step(5, "코드 리뷰", "생성된 코드에 대한 팀 피드백")
        
        result = self.a2a_call("mgx/team_discussion", {
            "project_id": project_id,
            "topic": "생성된 코드를 검토하고 개선점이나 추가 기능을 제안해주세요"
        })
        
        if result:
            print("🔍 코드 리뷰 완료!")
            print("\n💡 팀 피드백:")
            
            for i, discussion in enumerate(result['discussion'], 1):
                agent = discussion['agent']
                avatar = discussion['avatar']
                contribution = discussion['contribution']
                
                print(f"\n{i}. {avatar} {agent}:")
                print(f"   {contribution}")
                
                if i < len(result['discussion']):
                    time.sleep(1)
            
            input("\n📱 Press Enter to continue...")
            return result
        return None
    
    def project_status(self, project_id):
        """프로젝트 상태 확인"""
        self.step(6, "프로젝트 완료", "최종 결과를 확인합니다")
        
        result = self.a2a_call("mgx/project_status", {
            "project_id": project_id
        })
        
        if result:
            print(f"🎉 프로젝트 완료!")
            print(f"📂 제목: {result['title']}")
            print(f"📊 상태: {result['status']}")
            print(f"👥 할당된 에이전트: {', '.join(result['assigned_agents'])}")
            print(f"📅 생성일: {result['created_at']}")
            print(f"🎨 생성된 아티팩트: {result['artifacts_count']}개")
            print(f"💬 대화 메시지: {result['conversation_messages']}개")
            if result['latest_activity']:
                print(f"🕒 마지막 활동: {result['latest_activity']}")
            
            return result
        return None
    
    def run_full_demo(self):
        """전체 워크플로우 실행"""
        print("🚀 MGX 스타일 팀 협업 워크플로우 데모")
        print("Dream, Chat, Create - AI 팀과 함께 프로젝트를 만들어보세요!")
        print("\n💡 이 데모에서는:")
        print("   1. 팀 소개")
        print("   2. 프로젝트 생성")
        print("   3. 팀 토론")
        print("   4. 코드 생성")
        print("   5. 코드 리뷰")
        print("   6. 프로젝트 완료")
        
        input("\n📱 Press Enter to start...")
        
        # 1. 팀 소개
        self.show_team()
        
        # 2. 프로젝트 생성
        project_description = "현대적인 할 일 관리 웹 애플리케이션을 만들어주세요. 사용자 인증, 실시간 동기화, 팀 협업 기능이 포함되어야 합니다."
        project_id = self.create_project(project_description)
        
        if not project_id:
            print("❌ 프로젝트 생성에 실패했습니다.")
            return
        
        # 3. 첫 번째 팀 토론
        self.team_discussion(project_id, "이 프로젝트에 가장 적합한 기술 스택과 아키텍처는 무엇일까요?")
        
        # 4. 코드 생성
        artifact = self.generate_artifact(project_id, "React Todo 컴포넌트")
        
        # 5. 코드 리뷰
        self.follow_up_discussion(project_id)
        
        # 6. 프로젝트 상태
        self.project_status(project_id)
        
        print("\n🎊 데모 완료!")
        print("✨ 이것이 MGX 스타일의 AI 팀 협업 방식입니다!")
        print("\n🔗 다음 단계:")
        print("   • 다른 프로젝트로 실험해보기")
        print("   • 더 복잡한 컴포넌트 생성하기")  
        print("   • 팀 토론 주제 바꿔보기")

def main():
    """메인 실행 함수"""
    demo = MGXWorkflowDemo()
    
    try:
        # 서버 연결 확인
        response = demo.session.get(f"{demo.base_url}/health")
        if response.status_code != 200:
            print("❌ 서버에 연결할 수 없습니다. python run_server.py로 서버를 시작해주세요.")
            return
        
        demo.run_full_demo()
        
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다.")
        print("💡 다음 명령으로 서버를 시작해주세요: python run_server.py")
    except KeyboardInterrupt:
        print("\n👋 데모를 종료합니다.")
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main() 
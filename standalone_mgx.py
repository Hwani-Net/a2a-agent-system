#!/usr/bin/env python3
"""
의존성 없이 독립적으로 동작하는 MGX 팀 시뮬레이터
Cursor에서 바로 사용할 수 있는 간단한 AI 개발팀
"""
import random
import uuid
from datetime import datetime
import sys

class StandaloneMGX:
    def __init__(self):
        self.team_members = {
            "Mike": {
                "role": "팀 리더",
                "expertise": "프로젝트 관리, 팀 조율, 기술 전략",
                "description": "MGX 개발팀을 이끄는 경험 많은 리더",
                "status": "available"
            },
            "Alex": {
                "role": "시니어 개발자",
                "expertise": "React, Node.js, Python, 풀스택 개발",
                "description": "코드 생성과 아키텍처 설계의 전문가",
                "status": "available"
            },
            "Emma": {
                "role": "제품 관리자",
                "expertise": "제품 전략, 사용자 경험, 요구사항 분석",
                "description": "사용자 니즈를 기술적 솔루션으로 연결하는 브릿지",
                "status": "available"
            },
            "David": {
                "role": "데이터 분석가",
                "expertise": "데이터 과학, ML/AI, 성능 최적화",
                "description": "데이터 기반 의사결정과 인사이트 제공",
                "status": "available"
            },
            "Bob": {
                "role": "솔루션 아키텍트",
                "expertise": "시스템 설계, 클라우드 아키텍처, 확장성",
                "description": "확장 가능한 시스템 아키텍처 설계 전문가",
                "status": "available"
            },
            "Sophia": {
                "role": "UI/UX 디자이너",
                "expertise": "사용자 인터페이스, 사용자 경험, 디자인 시스템",
                "description": "직관적이고 아름다운 사용자 경험 창조",
                "status": "available"
            }
        }
        
        self.current_project = None
        self.chat_history = []
    
    def show_team(self):
        """팀 정보 표시"""
        print("👥 MGX AI 개발팀:")
        print("="*50)
        
        for name, info in self.team_members.items():
            status = "🟢" if info['status'] == 'available' else "🔴"
            print(f"{status} {name} - {info['role']}")
            print(f"   💪 {info['expertise']}")
            print(f"   📝 {info['description']}")
            print()
    
    def create_project(self, project_name, description=""):
        """프로젝트 생성"""
        project_id = str(uuid.uuid4())
        
        self.current_project = {
            "project_id": project_id,
            "name": project_name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "team_assignments": ["Mike", "Alex", "Emma"],
            "artifacts": []
        }
        
        print(f"🎯 프로젝트 '{project_name}' 생성 완료!")
        print(f"   📋 프로젝트 ID: {project_id}")
        print(f"   👥 담당팀: {', '.join(self.current_project['team_assignments'])}")
        print(f"   📅 생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        return self.current_project
    
    def generate_code(self, description):
        """코드 생성 시뮬레이션"""
        if not self.current_project:
            # 임시 프로젝트 생성
            self.create_project(f"빠른작업-{datetime.now().strftime('%H%M%S')}", "임시 코드 생성")
        
        print(f"⚡ Alex가 '{description}' 코드를 생성합니다...")
        
        # 코드 템플릿들
        code_templates = {
            "react": self._react_component_template(description),
            "fastapi": self._fastapi_template(description),
            "python": self._python_function_template(description),
            "html": self._html_template(description)
        }
        
        # 키워드 기반으로 적절한 템플릿 선택
        desc_lower = description.lower()
        if any(word in desc_lower for word in ['react', '컴포넌트', 'component']):
            code_type = "react"
            filename = f"{description.replace(' ', '_')}.jsx"
        elif any(word in desc_lower for word in ['fastapi', 'api', 'rest']):
            code_type = "fastapi"
            filename = f"{description.replace(' ', '_')}.py"
        elif any(word in desc_lower for word in ['html', '웹페이지', 'webpage']):
            code_type = "html"
            filename = f"{description.replace(' ', '_')}.html"
        else:
            code_type = "python"
            filename = f"{description.replace(' ', '_')}.py"
        
        generated_code = code_templates[code_type]
        
        # 아티팩트 저장
        artifact = {
            "artifact_id": str(uuid.uuid4()),
            "type": "code",
            "content": generated_code,
            "created_by": "Alex",
            "created_at": datetime.now().isoformat(),
            "metadata": {
                "filename": filename,
                "language": code_type,
                "description": description
            }
        }
        
        self.current_project["artifacts"].append(artifact)
        
        print(f"\n💻 생성된 코드:")
        print(f"  📁 파일: {filename}")
        print(f"  🔧 언어: {code_type}")
        print(f"  📏 크기: {len(generated_code)} 문자")
        print(f"  👨‍💻 작성자: Alex")
        print("\n" + "="*60)
        print(generated_code)
        print("="*60)
        
        return artifact
    
    def start_discussion(self, topic):
        """팀 토론 시뮬레이션"""
        if not self.current_project:
            self.create_project(f"토론-{datetime.now().strftime('%H%M%S')}", "팀 토론")
        
        print(f"💬 '{topic}'에 대한 팀 토론을 시작합니다...")
        
        # 미리 정의된 토론 응답들
        discussion_responses = {
            "Mike": f"'{topic}'에 대해 팀원들과 논의해보겠습니다. 프로젝트 목표와 일치하는지 확인이 필요합니다.",
            "Emma": f"사용자 관점에서 {topic}는 매우 중요한 요소입니다. UX를 고려한 접근이 필요해요.",
            "Alex": f"{topic} 구현을 위해서는 최신 기술 스택을 활용하는 것이 좋겠습니다.",
            "Sophia": f"디자인 관점에서 {topic}는 직관적이고 아름다운 인터페이스가 필요합니다."
        }
        
        print(f"\n🎯 토론 결과:")
        for name, response in discussion_responses.items():
            print(f"  💭 {name}: {response}")
        
        # 결정사항 생성
        decisions = [
            f"{topic}에 대한 구체적인 계획 수립",
            "팀원들 간의 역할 분담 확정",
            "다음 단계 액션 아이템 정의"
        ]
        
        print(f"\n📋 팀 결정사항:")
        for decision in decisions:
            print(f"  ✅ {decision}")
        
        return {
            "topic": topic,
            "participants": list(discussion_responses.keys()),
            "comments": [{"author": k, "content": v} for k, v in discussion_responses.items()],
            "decisions": decisions
        }
    
    def quick_action(self, user_request):
        """사용자 요청을 분석하고 적절한 액션 실행"""
        print(f"🚀 MGX 팀이 '{user_request}' 요청을 처리합니다...\n")
        
        request_lower = user_request.lower()
        
        if any(word in request_lower for word in ['팀', 'team', '소개', '누구']):
            self.show_team()
        elif any(word in request_lower for word in ['프로젝트', 'project', '만들어', 'create']):
            project_name = f"사용자 요청 프로젝트 - {datetime.now().strftime('%H:%M')}"
            self.create_project(project_name, user_request)
            # 바로 코드도 생성
            self.generate_code(user_request)
        elif any(word in request_lower for word in ['토론', 'discuss', '의견', '생각']):
            self.start_discussion(user_request)
        else:
            # 기본적으로 코드 생성
            self.generate_code(user_request)
    
    # 코드 템플릿들
    def _react_component_template(self, description):
        component_name = description.replace(' ', '').replace('컴포넌트', '').replace('Component', '') or "MyComponent"
        return f"""import React, {{ useState }} from 'react';

const {component_name} = () => {{
    const [state, setState] = useState('');

    const handleAction = () => {{
        // {description} 로직 구현
        console.log('{description} 동작 실행');
    }};

    return (
        <div className="{component_name.lower()}">
            <h2>{description}</h2>
            <input 
                type="text" 
                value={{state}}
                onChange={{(e) => setState(e.target.value)}}
                placeholder="입력하세요"
            />
            <button onClick={{handleAction}}>
                실행
            </button>
        </div>
    );
}};

export default {component_name};"""

    def _fastapi_template(self, description):
        return f"""from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="{description} API")

class RequestModel(BaseModel):
    data: str
    timestamp: datetime = None

class ResponseModel(BaseModel):
    success: bool
    message: str
    result: dict

@app.get("/")
async def root():
    return {{"message": "{description} API 서버"}}

@app.post("/api/action", response_model=ResponseModel)
async def perform_action(request: RequestModel):
    try:
        # {description} 로직 구현
        result = {{
            "processed_data": request.data,
            "timestamp": datetime.now(),
            "action": "{description}"
        }}
        
        return ResponseModel(
            success=True,
            message="{description} 성공적으로 처리됨",
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)"""

    def _python_function_template(self, description):
        function_name = description.replace(' ', '_').replace('함수', '').replace('기능', '') or "my_function"
        return f"""#!/usr/bin/env python3
\"\"\"
{description} 구현
\"\"\"
from datetime import datetime
from typing import List, Dict, Any

def {function_name}(data: Any) -> Dict[str, Any]:
    \"\"\"
    {description}를 수행하는 함수
    
    Args:
        data: 입력 데이터
        
    Returns:
        처리 결과를 담은 딕셔너리
    \"\"\"
    try:
        # {description} 로직 구현
        result = {{
            "input": data,
            "processed_at": datetime.now().isoformat(),
            "success": True,
            "message": "{description} 처리 완료"
        }}
        
        return result
        
    except Exception as e:
        return {{
            "success": False,
            "error": str(e),
            "message": "{description} 처리 실패"
        }}

def main():
    \"\"\"메인 실행 함수\"\"\"
    test_data = "테스트 데이터"
    result = {function_name}(test_data)
    print(f"결과: {{result}}")

if __name__ == "__main__":
    main()"""

    def _html_template(self, description):
        return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{description}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        .content {{
            line-height: 1.6;
            color: #666;
        }}
        .action-btn {{
            background: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        .action-btn:hover {{
            background: #0056b3;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{description}</h1>
        <div class="content">
            <p>{description}를 위한 웹페이지입니다.</p>
            <p>이곳에 원하는 콘텐츠를 추가하세요.</p>
            <button class="action-btn" onclick="performAction()">실행</button>
        </div>
    </div>

    <script>
        function performAction() {{
            alert('{description} 기능이 실행되었습니다!');
            console.log('{description} 동작 완료');
        }}
    </script>
</body>
</html>"""

def main():
    if len(sys.argv) < 2:
        print("🚀 MGX AI 개발팀 - 독립형 버전")
        print("="*50)
        print("사용법:")
        print("  python standalone_mgx.py \"요청 내용\"")
        print("\n📝 예시:")
        print("  python standalone_mgx.py \"팀 소개해줘\"")
        print("  python standalone_mgx.py \"React 로그인 컴포넌트 만들어줘\"")
        print("  python standalone_mgx.py \"FastAPI REST API 만들어줘\"")
        print("  python standalone_mgx.py \"Python 데이터 처리 함수 만들어줘\"")
        print("  python standalone_mgx.py \"HTML 랜딩페이지 만들어줘\"")
        print("  python standalone_mgx.py \"데이터베이스 설계에 대해 토론해줘\"")
        return
    
    user_request = " ".join(sys.argv[1:])
    mgx = StandaloneMGX()
    mgx.quick_action(user_request)

if __name__ == "__main__":
    main() 
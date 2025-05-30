# 🚀 MGX 스타일 AI 팀 협업 실행 가이드

## 📋 목차

1. [기본 설정](#기본-설정)
2. [팀 소개](#팀-소개)
3. [프로젝트 생성](#프로젝트-생성)
4. [팀 토론](#팀-토론)
5. [코드 생성](#코드-생성)
6. [프로젝트 관리](#프로젝트-관리)
7. [실제 사용 예시](#실제-사용-예시)

## 🎯 기본 설정

### 1. 서버 시작

```powershell
cd my_agent_system
python run_server.py
```

### 2. 서버 상태 확인

```powershell
python -c "import requests; print('서버 상태:', requests.get('http://localhost:8000/health').json()['status'])"
```

## 👥 팀 소개

### 우리의 24/7 AI 개발팀

- **👨‍💼 Mike** - 팀 리더 (프로젝트 관리, 전략 기획)
- **👨‍💻 Alex** - 엔지니어 (풀스택 개발, DevOps)
- **👩‍💼 Emma** - 제품 매니저 (UX 연구, 기능 기획)
- **👨‍🔬 David** - 데이터 분석가 (머신러닝, 분석)
- **👨‍🏗️ Bob** - 아키텍트 (시스템 설계, 확장성)
- **👩‍🎨 Sophia** - UI 디자이너 (인터페이스 설계)

### 팀 정보 조회

```powershell
python -c "
import requests, json
response = requests.post('http://localhost:8000/a2a', json={
    'jsonrpc': '2.0', 
    'method': 'mgx/team_info', 
    'id': '1'
})
team = response.json()['result']
print(f'팀: {team[\"team_name\"]}')
print('멤버들:')
for member in team['members']:
    print(f'  {member[\"avatar\"]} {member[\"name\"]} - {member[\"role\"]}')
"
```

## 🏗️ 프로젝트 생성

### 1. 새 프로젝트 시작

```powershell
python -c "
import requests, json
response = requests.post('http://localhost:8000/a2a', json={
    'jsonrpc': '2.0',
    'method': 'mgx/create_project',
    'params': {
        'description': '현대적인 할 일 관리 웹 애플리케이션을 만들어주세요. 사용자 인증, 실시간 동기화, 팀 협업 기능 포함',
        'user_id': 'demo_user'
    },
    'id': '2'
})
result = response.json()['result']
print(f'프로젝트 생성 완료!')
print(f'ID: {result[\"project_id\"]}')
print(f'상태: {result[\"status\"]}')
print(f'메시지: {result[\"message\"]}')
"
```

### 2. 프로젝트 ID 저장 (다음 단계에서 사용)

위에서 생성된 `project_id`를 복사해두세요. 예: `abedb90f-656b-4fc3-a3df-60c0caf50e86`

## 💬 팀 토론

### 1. 기술 스택 논의

```powershell
python -c "
import requests, json
PROJECT_ID = 'YOUR_PROJECT_ID_HERE'  # 위에서 생성한 ID로 변경
response = requests.post('http://localhost:8000/a2a', json={
    'jsonrpc': '2.0',
    'method': 'mgx/team_discussion',
    'params': {
        'project_id': PROJECT_ID,
        'topic': '이 프로젝트에 가장 적합한 기술 스택과 아키텍처는 무엇일까요?'
    },
    'id': '3'
})
discussion = response.json()['result']
print(f'토론 주제: {discussion[\"topic\"]}')
print(f'참여자: {discussion[\"participants\"]}명')
print('팀 의견:')
for i, msg in enumerate(discussion['discussion'], 1):
    print(f'{i}. {msg[\"avatar\"]} {msg[\"agent\"]}: {msg[\"contribution\"]}')
"
```

### 2. 상세 기능 논의

```powershell
python -c "
import requests, json
PROJECT_ID = 'YOUR_PROJECT_ID_HERE'
response = requests.post('http://localhost:8000/a2a', json={
    'jsonrpc': '2.0',
    'method': 'mgx/team_discussion',
    'params': {
        'project_id': PROJECT_ID,
        'topic': '사용자 인증과 실시간 동기화를 어떻게 구현할까요?'
    },
    'id': '4'
})
discussion = response.json()['result']
print('=== 상세 기능 논의 ===')
for msg in discussion['discussion']:
    print(f'{msg[\"avatar\"]} {msg[\"agent\"]}: {msg[\"contribution\"]}')
"
```

## ⚡ 코드 생성

### 1. React 컴포넌트 생성

```powershell
python -c "
import requests, json
PROJECT_ID = 'YOUR_PROJECT_ID_HERE'
response = requests.post('http://localhost:8000/a2a', json={
    'jsonrpc': '2.0',
    'method': 'mgx/generate_artifact',
    'params': {
        'project_id': PROJECT_ID,
        'component_type': 'React Todo 컴포넌트'
    },
    'id': '5'
})
result = response.json()['result']
artifact = result['artifact']
print(f'✅ {result[\"message\"]}')
print(f'📝 타입: {artifact[\"component_type\"]}')
print(f'👨‍💻 작성자: {artifact[\"created_by\"]}')
print(f'📅 생성일: {artifact[\"created_at\"]}')
print()
print('📋 생성된 코드:')
print(artifact['content'][:800] + '...')
"
```

### 2. 백엔드 API 생성

```powershell
python -c "
import requests, json
PROJECT_ID = 'YOUR_PROJECT_ID_HERE'
response = requests.post('http://localhost:8000/a2a', json={
    'jsonrpc': '2.0',
    'method': 'mgx/generate_artifact',
    'params': {
        'project_id': PROJECT_ID,
        'component_type': 'FastAPI 백엔드 서버'
    },
    'id': '6'
})
result = response.json()['result']
artifact = result['artifact']
print(f'✅ 백엔드 코드 생성 완료!')
print(f'📋 코드 미리보기:')
print(artifact['content'][:500] + '...')
"
```

## 📊 프로젝트 관리

### 1. 프로젝트 상태 확인

```powershell
python -c "
import requests, json
PROJECT_ID = 'YOUR_PROJECT_ID_HERE'
response = requests.post('http://localhost:8000/a2a', json={
    'jsonrpc': '2.0',
    'method': 'mgx/project_status',
    'params': {
        'project_id': PROJECT_ID
    },
    'id': '7'
})
status = response.json()['result']
print('🎉 프로젝트 현황')
print(f'📂 제목: {status[\"title\"]}')
print(f'📊 상태: {status[\"status\"]}')
print(f'👥 할당된 에이전트: {status[\"assigned_agents\"]}')
print(f'🎨 생성된 아티팩트: {status[\"artifacts_count\"]}개')
print(f'💬 대화 메시지: {status[\"conversation_messages\"]}개')
print(f'🕒 마지막 활동: {status[\"latest_activity\"]}')
"
```

## 🎮 실제 사용 예시

### 🌟 완전한 워크플로우 예시

```powershell
# 1. 팀 확인
python -c "print('=== 1단계: 팀 확인 ==='); import requests; team = requests.post('http://localhost:8000/a2a', json={'jsonrpc': '2.0', 'method': 'mgx/team_info', 'id': '1'}).json()['result']; print(f'팀: {team[\"team_name\"]} ({len(team[\"members\"])}명)')"

# 2. 프로젝트 생성
python -c "print('\\n=== 2단계: 프로젝트 생성 ==='); import requests; project = requests.post('http://localhost:8000/a2a', json={'jsonrpc': '2.0', 'method': 'mgx/create_project', 'params': {'description': '온라인 쇼핑몰 플랫폼'}, 'id': '2'}).json()['result']; print(f'프로젝트 ID: {project[\"project_id\"]}'); print('**이 ID를 복사해서 다음 명령어에 사용하세요**')"

# 3. 토론 (위에서 복사한 PROJECT_ID 사용)
# python -c "PROJECT_ID='YOUR_ID_HERE'; print('\\n=== 3단계: 팀 토론 ==='); import requests; discussion = requests.post('http://localhost:8000/a2a', json={'jsonrpc': '2.0', 'method': 'mgx/team_discussion', 'params': {'project_id': PROJECT_ID, 'topic': '전자상거래 플랫폼의 핵심 기능은?'}, 'id': '3'}).json()['result']; [print(f'{msg[\"avatar\"]} {msg[\"agent\"]}: {msg[\"contribution\"]}') for msg in discussion['discussion']]"

# 4. 코드 생성
# python -c "PROJECT_ID='YOUR_ID_HERE'; print('\\n=== 4단계: 코드 생성 ==='); import requests; artifact = requests.post('http://localhost:8000/a2a', json={'jsonrpc': '2.0', 'method': 'mgx/generate_artifact', 'params': {'project_id': PROJECT_ID, 'component_type': '상품 목록 컴포넌트'}, 'id': '4'}).json()['result']['artifact']; print(f'생성된 코드 ({artifact[\"component_type\"]}):'); print(artifact['content'][:400] + '...')"
```

### 📱 Quick Test Scripts

#### 빠른 테스트

```powershell
python quick_mgx_test.py
```

#### 간단한 테스트  

```powershell
python simple_test.py
```

#### 전체 워크플로우 (대화형)

```powershell
python mgx_workflow_demo.py
```

## 💡 사용 팁

### 1. 프로젝트 아이디어 예시

- "AI 기반 개인 비서 앱"
- "실시간 협업 화이트보드"
- "암호화폐 포트폴리오 트래커"
- "소셜 미디어 분석 도구"
- "IoT 스마트 홈 시스템"

### 2. 토론 주제 예시

- "확장성을 위한 최적의 아키텍처는?"
- "사용자 경험을 개선하는 방법은?"
- "보안을 강화하는 방안은?"
- "성능 최적화 전략은?"
- "배포 및 운영 방안은?"

### 3. 컴포넌트 타입 예시

- "React 로그인 컴포넌트"
- "FastAPI 사용자 인증"
- "MongoDB 데이터 모델"
- "Vue.js 대시보드"
- "Python 데이터 처리"

## 🎯 다음 단계

1. **자신만의 프로젝트 만들기**
2. **다양한 토론 주제로 실험**
3. **여러 컴포넌트 생성해보기**
4. **A2A 프로토콜로 다른 에이전트와 연결**

---

## 🌟 MGX vs 전통적 개발

| 구분 | 전통적 개발 | MGX 스타일 |
|------|-------------|------------|
| 팀 구성 | 개별 개발자들 | AI 에이전트 팀 |
| 의사결정 | 회의, 이메일 | 실시간 AI 토론 |
| 코드 생성 | 수동 코딩 | AI 자동 생성 |
| 24/7 가용성 | ❌ | ✅ |
| 즉석 전문성 | ❌ | ✅ (6개 분야) |
| 확장성 | 제한적 | 무제한 |

**MGX = Magic Experience (마법같은 경험) 🪄**

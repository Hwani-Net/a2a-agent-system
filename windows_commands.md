# Windows에서 A2A MGX 서버 테스트하기

WSL 설치가 완료되었으며, 이제 다양한 방법으로 A2A 서버를 테스트할 수 있습니다.

## 🔧 Windows 네이티브 명령어

### 1. Python requests 사용 (가장 안정적)

#### 서버 상태 확인

```powershell
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

#### Agent Card 조회

```powershell
python -c "import requests; import json; response = requests.get('http://localhost:8000/agent-card'); print(json.dumps(response.json()['identity'], indent=2, ensure_ascii=False))"
```

#### MGX 팀 정보 조회 (A2A Protocol)

```powershell
python -c "import requests; import json; payload = {'jsonrpc': '2.0', 'method': 'mgx/team_info', 'id': '1'}; response = requests.post('http://localhost:8000/a2a', json=payload); print(json.dumps(response.json()['result'], indent=2, ensure_ascii=False))"
```

### 2. PowerShell Invoke-RestMethod (단순한 GET 요청)

#### 서버 상태 확인

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

#### Agent Card 조회

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/agent-card"
```

## 🐧 WSL에서 curl 사용

WSL이 설치되었으므로 이제 Linux 명령어도 사용할 수 있습니다:

#### 서버 상태 확인

```powershell
wsl curl http://localhost:8000/health
```

#### Agent Card 조회

```powershell
wsl curl http://localhost:8000/agent-card
```

#### MGX 팀 정보 조회 (A2A Protocol)

```powershell
wsl curl -X POST http://localhost:8000/a2a -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"mgx/team_info","id":"1"}'
```

#### MGX 프로젝트 생성

```powershell
wsl curl -X POST http://localhost:8000/a2a -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"mgx/create_project","params":{"description":"Create a modern todo app","user_id":"test"},"id":"2"}'
```

## 🚀 테스트 스크립트 사용

가장 쉬운 방법은 제공된 테스트 스크립트를 사용하는 것입니다:

```powershell
# 간단한 테스트
python simple_test.py

# 전체 MGX 기능 테스트
python test_mgx_features.py simple

# 대화형 테스트
python simple_chat.py
```

## 🌟 MGX 스타일 기능 테스트

### 1. 팀 정보 조회

```python
import requests
payload = {"jsonrpc": "2.0", "method": "mgx/team_info", "id": "1"}
response = requests.post("http://localhost:8000/a2a", json=payload)
team_info = response.json()["result"]
print(f"Team: {team_info['team_name']}")
for member in team_info['members']:
    print(f"{member['avatar']} {member['name']} - {member['role']}")
```

### 2. 프로젝트 생성

```python
import requests
payload = {
    "jsonrpc": "2.0", 
    "method": "mgx/create_project", 
    "params": {"description": "Build a calculator app"}, 
    "id": "2"
}
response = requests.post("http://localhost:8000/a2a", json=payload)
project = response.json()["result"]
print(f"Project ID: {project['project_id']}")
```

### 3. 팀 토론

```python
import requests
payload = {
    "jsonrpc": "2.0",
    "method": "mgx/team_discussion",
    "params": {
        "project_id": "your-project-id",
        "topic": "What's the best tech stack?"
    },
    "id": "3"
}
response = requests.post("http://localhost:8000/a2a", json=payload)
discussion = response.json()["result"]
for msg in discussion['discussion']:
    print(f"{msg['avatar']} {msg['agent']}: {msg['contribution']}")
```

## 🛠️ 서버 관리

### 서버 시작

```powershell
python run_server.py
```

### 백그라운드로 서버 시작 (Windows)

```powershell
Start-Process python -ArgumentList "run_server.py" -WindowStyle Hidden
```

### 서버 프로세스 확인

```powershell
Get-Process python
```

### 서버 종료 (특정 포트)

```powershell
netstat -ano | findstr :8000
# PID를 확인한 후
taskkill /PID <PID> /F
```

## 📊 성능 및 상태 모니터링

### 서버 응답 시간 측정

```powershell
Measure-Command { Invoke-RestMethod -Uri "http://localhost:8000/health" }
```

### 서버 로그 확인 (Python 프로세스)

```powershell
Get-Process python | Select-Object Id,ProcessName,CPU,WorkingSet
```

## 🎯 권장 워크플로우

1. **서버 시작**: `python run_server.py`
2. **기본 테스트**: `python simple_test.py`
3. **MGX 기능 테스트**: `python test_mgx_features.py simple`
4. **대화형 테스트**: `python simple_chat.py`

이제 WSL 설치가 완료되어 curl도 사용할 수 있지만, Windows 환경에서는 Python requests가 가장 안정적이고 편리합니다!

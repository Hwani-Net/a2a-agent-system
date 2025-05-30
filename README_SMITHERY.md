# 🔄 Crew Sync Agent - Dynamic Team Collaboration MCP

**Smithery 배포를 위한 다이나믹 팀 협업 시스템**

## 🌟 주요 특징

- **🔄 동적 크루 동기화**: 유연한 팀 구성으로 프로젝트별 최적화
- **👥 확장 가능한 팀**: 최대 10명까지 동적 팀 멤버 추가/관리
- **🎯 우선순위 기반**: Low/Medium/High/Urgent 우선순위 설정
- **🔐 보안 강화**: API 키 환경 변수 관리로 안전한 배포
- **⚡ 실시간 협업**: MCP 프로토콜 기반 즉시 팀 동기화

## 🏗️ 기본 크루 구성 (확장 가능)

- **🎯 Taylor**: Team Coordinator - 전략 기획 및 프로젝트 조정
- **⚡ Jordan**: Tech Engineer - 풀스택 개발 및 DevOps  
- **💡 Riley**: Product Strategist - UX 연구 및 기능 기획
- **📊 Casey**: Data Specialist - ML, 분석 및 시각화
- **🏗️ Morgan**: System Architect - 시스템 설계 및 확장성
- **🎨 Avery**: Design Lead - 인터페이스 디자인 및 프로토타이핑

> **Note**: 팀 구성은 완전히 동적이며, 프로젝트 요구사항에 따라 조정 가능합니다.

## 🛠️ 사용 가능한 도구

### 1. `sync_crew` - 크루 동기화

```json
{
  "task": "작업 설명",
  "crew_members": ["Taylor", "Jordan", "Riley"], // 선택사항
  "priority": "high" // low/medium/high/urgent
}
```

### 2. `add_crew_member` - 새 크루 멤버 추가

```json
{
  "name": "새 멤버 이름",
  "role": "역할 및 전문 분야 설명"
}
```

### 3. `list_crew` - 현재 크루 멤버 조회

```json
{} // 파라미터 없음
```

### 4. `echo` - 연결 테스트

```json
{
  "text": "테스트 메시지"
}
```

## 🚀 Smithery 배포 가이드

### 1. 레포지토리 준비

```bash
# GitHub 레포지토리 생성 및 푸시
git init
git add .
git commit -m "Initial Crew Sync Agent setup"
git branch -M main
git remote add origin https://github.com/your-username/crew-sync-agent.git
git push -u origin main
```

### 2. Smithery 배포

```bash
# smithery CLI 설치
npm install -g smithery

# Smithery에 배포
smithery deploy https://github.com/your-username/crew-sync-agent
```

### 3. 환경 변수 설정

Smithery 대시보드에서 다음 환경 변수들을 설정:

- `OPENAI_API_KEY`: OpenAI API 키 (선택사항)
- `ANTHROPIC_API_KEY`: Anthropic API 키 (선택사항)
- `GOOGLE_API_KEY`: Google API 키 (선택사항)
- `COHERE_API_KEY`: Cohere API 키 (선택사항)
- `AI_SERVICE`: 기본 AI 서비스 (openai/anthropic/google/cohere)
- `MODEL_NAME`: 기본 모델명 (예: gpt-4)
- `MAX_CREW_SIZE`: 최대 크루 크기 (기본값: 10)

## 🧪 로컬 테스트

### 전체 기능 테스트

```bash
python test_crew_sync.py
```

### 개별 도구 테스트

```bash
# 크루 멤버 조회
python -c "
import json, subprocess, sys
req = {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': 'list_crew', 'arguments': {}}}
subprocess.run([sys.executable, 'mcp_server.py'], input=json.dumps(req), text=True)
"
```

## 📋 사용 예시

### 예시 1: 웹 개발 프로젝트

```json
{
  "task": "React + Node.js 전자상거래 플랫폼 개발",
  "crew_members": ["Jordan", "Riley", "Avery"],
  "priority": "high"
}
```

### 예시 2: 데이터 분석 프로젝트  

```json
{
  "task": "사용자 행동 패턴 분석 및 예측 모델 구축",
  "crew_members": ["Casey", "Morgan"],
  "priority": "medium"
}
```

### 예시 3: 새 전문가 추가

```json
{
  "name": "Alex",
  "role": "Security Specialist - 사이버보안 및 컴플라이언스 전문가"
}
```

## 🔧 고급 설정

### 팀 크기 확장

환경 변수 `MAX_CREW_SIZE`를 조정하여 더 큰 팀 구성 가능:

```bash
# 최대 20명까지 확장
export MAX_CREW_SIZE=20
```

### 커스텀 AI 모델 사용

```bash
export AI_SERVICE=anthropic
export MODEL_NAME=claude-3-sonnet
```

## 🛡️ 보안 고려사항

- ✅ API 키는 환경 변수로만 관리
- ✅ 코드에 하드코딩된 키 없음
- ✅ Docker 컨테이너 비루트 사용자 실행
- ✅ 민감한 파일 `.dockerignore`로 제외
- ✅ MCP 프로토콜 표준 준수

## 📞 지원 및 문의

- **GitHub Issues**: 버그 리포트 및 기능 요청
- **문서**: Smithery 공식 문서 참조
- **커뮤니티**: MCP 개발자 커뮤니티 참여

---

**Crew Sync Agent**: 유연하고 확장 가능한 AI 팀 협업 솔루션 🚀

# A2A Agent System - Smithery MCP Deployment Guide

이 가이드는 Smithery를 통해 A2A (Agent2Agent) 호환 AI 에이전트 시스템을 MCP (Model Context Protocol) 서버로 배포하는 방법을 설명합니다.

## 🔐 보안 원칙

**중요**: 이 배포 방법은 API 키를 안전하게 처리합니다.

- ✅ **환경 변수로 API 키 관리** - 코드에 하드코딩되지 않음
- ✅ **Smithery가 런타임에 키 주입** - 안전한 시크릿 관리
- ✅ **API 키 로깅 방지** - 민감한 정보 노출 차단
- ✅ **Docker 이미지에 키 포함 안 됨** - `.dockerignore`로 보호

## 📦 배포 구성 요소

```
my_agent_system/
├── Dockerfile              # Docker 컨테이너 정의
├── .dockerignore           # 민감한 파일 제외
├── smithery.json           # Smithery MCP 서버 메타데이터
├── config_secure.py        # 보안 강화된 설정
├── mcp_server.py          # MCP 서버 구현
├── requirements.txt       # Python 의존성
└── README_SMITHERY.md     # 이 파일
```

## 🚀 Smithery 배포 단계

### 1. 필수 준비사항

- Docker 설치
- GitHub 계정 (코드 저장소용)
- Smithery 계정
- 필요한 API 키들 (선택사항):
    - `OPENAI_API_KEY` - OpenAI GPT 모델용
    - `ANTHROPIC_API_KEY` - Claude 모델용  
    - `PERPLEXITY_API_KEY` - 웹 검색용
    - `SERPER_API_KEY` - 대체 웹 검색용
    - `OPENWEATHER_API_KEY` - 날씨 정보용

### 2. 코드 저장소 준비

```bash
# GitHub에 새 저장소 생성 후
git clone https://github.com/yourusername/a2a-mcp-server.git
cd a2a-mcp-server

# A2A 에이전트 시스템 파일들 복사
cp -r /path/to/my_agent_system/* .

# Git에 추가
git add .
git commit -m "Initial A2A MCP server implementation"
git push origin main
```

### 3. Docker 이미지 빌드 테스트

```bash
# 로컬에서 Docker 이미지 빌드
docker build -t a2a-mcp-server .

# 컨테이너 테스트 (API 키 없이)
docker run --rm -it a2a-mcp-server

# API 키와 함께 테스트
docker run --rm -it \
  -e OPENAI_API_KEY="your-openai-key" \
  -e ANTHROPIC_API_KEY="your-anthropic-key" \
  a2a-mcp-server
```

### 4. Smithery에 배포

#### 방법 1: Smithery CLI 사용

```bash
# Smithery CLI 설치
npm install -g @smithery/cli

# 로그인
smithery login

# MCP 서버 배포
smithery deploy --config smithery.json
```

#### 방법 2: Smithery 웹 인터페이스

1. [Smithery 대시보드](https://smithery.ai) 접속
2. "New MCP Server" 클릭
3. GitHub 저장소 연결
4. `smithery.json` 설정 확인
5. 환경 변수 설정 (API 키들)
6. 배포 실행

### 5. 환경 변수 설정

Smithery 대시보드에서 다음 환경 변수들을 안전하게 설정:

```
OPENAI_API_KEY=sk-proj-xxx...          # OpenAI API 키
ANTHROPIC_API_KEY=sk-ant-xxx...        # Anthropic API 키  
PERPLEXITY_API_KEY=pplx-xxx...         # Perplexity API 키
SERPER_API_KEY=xxx...                  # Serper API 키
OPENWEATHER_API_KEY=xxx...             # OpenWeatherMap API 키
DEPLOYMENT_ENV=production              # 배포 환경
LOG_LEVEL=INFO                         # 로그 레벨
```

**주의**: 이 키들은 Smithery의 시크릿 관리 시스템에 안전하게 저장됩니다.

## 🔧 MCP 클라이언트 연결

배포 후 Claude Desktop이나 다른 MCP 클라이언트에서 사용:

### Claude Desktop 설정 (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "a2a-agent-system": {
      "command": "docker",
      "args": [
        "run",
        "--rm", 
        "-i",
        "smithery.ai/your-username/a2a-mcp-server:latest"
      ]
    }
  }
}
```

### 또는 Smithery URL 직접 사용

```json
{
  "mcpServers": {
    "a2a-agent-system": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/mcp-client@latest",
        "connect",
        "https://smithery.ai/api/mcp/your-username/a2a-mcp-server"
      ]
    }
  }
}
```

## 🛠 사용 가능한 도구들

배포된 MCP 서버는 다음 도구들을 제공합니다:

### 텍스트 생성

```python
# 사용 가능한 경우: OpenAI 또는 Anthropic API 키 설정시
await mcp_client.call_tool("generate_text", {
    "prompt": "AI의 미래에 대해 설명해주세요",
    "max_tokens": 500
})
```

### 텍스트 분석  

```python
await mcp_client.call_tool("analyze_text", {
    "text": "분석할 텍스트 내용",
    "analysis_type": "sentiment"
})
```

### 웹 검색

```python
# 사용 가능한 경우: Perplexity 또는 Serper API 키 설정시
await mcp_client.call_tool("web_search", {
    "query": "최신 AI 뉴스",
    "max_results": 5
})
```

### 날씨 정보

```python
# 사용 가능한 경우: OpenWeatherMap API 키 설정시
await mcp_client.call_tool("get_weather", {
    "location": "Seoul, South Korea"
})
```

## 📊 모니터링 및 상태 확인

### 리소스 조회

```python
# 에이전트 카드 정보
agent_card = await mcp_client.read_resource("agent://card")

# 서버 상태
status = await mcp_client.read_resource("agent://status")

# 설정 정보 (민감한 정보 제외)
config = await mcp_client.read_resource("agent://config") 
```

### 헬스 체크

```bash
# Docker 컨테이너 상태 확인
docker ps

# 로그 확인
docker logs <container-id>

# Smithery 대시보드에서 메트릭 확인
```

## 🔍 문제 해결

### 일반적인 문제들

1. **API 키 오류**
   - Smithery 대시보드에서 환경 변수 올바르게 설정되었는지 확인
   - 키 형식이 올바른지 확인 (`sk-proj-`, `sk-ant-` 등)

2. **Docker 빌드 실패**
   - `.dockerignore`에 불필요한 파일들이 포함되었는지 확인
   - `requirements.txt`의 의존성이 올바른지 확인

3. **MCP 연결 실패**
   - 컨테이너가 정상적으로 실행되고 있는지 확인
   - STDIO 모드로 통신하는지 확인

### 로그 분석

```bash
# Smithery 로그 확인
smithery logs a2a-mcp-server

# 로컬 Docker 로그
docker logs -f <container-name>
```

## 🔄 업데이트 및 버전 관리

### 새 버전 배포

```bash
# 코드 업데이트 후
git add .
git commit -m "Update A2A MCP server v1.1.0"
git tag v1.1.0
git push origin main --tags

# Smithery에서 자동 재배포 또는 수동 트리거
smithery deploy --tag v1.1.0
```

### 롤백

```bash
# 이전 버전으로 롤백
smithery rollback a2a-mcp-server --to-version v1.0.0
```

## 📚 추가 리소스

- [Smithery 공식 문서](https://smithery.ai/docs/)
- [MCP 사양](https://modelcontextprotocol.io/)
- [A2A 프로토콜 문서](https://a2a.to/)
- [Docker 보안 가이드](https://docs.docker.com/engine/security/)

## 🤝 지원

문제가 발생하면:

1. [GitHub Issues](https://github.com/yourusername/a2a-mcp-server/issues)에 신고
2. [Smithery 지원팀](https://smithery.ai/support) 문의  
3. A2A 커뮤니티 포럼 참여

---

**보안 알림**: API 키는 절대 코드 저장소에 커밋하지 마세요. 항상 환경 변수나 시크릿 관리 시스템을 사용하세요.

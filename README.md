# A2A Agent System with MGX-Inspired Team Collaboration

[![smithery badge](https://smithery.ai/badge/@Hwani-Net/a2a-agent-system)](https://smithery.ai/server/@Hwani-Net/a2a-agent-system)

A comprehensive **Agent-to-Agent (A2A)** protocol implementation featuring **MGX-inspired multi-agent team collaboration**. This system combines the power of A2A interoperability with the innovative team-based approach found in MGX (<https://mgx.dev/>).

## 🌟 New MGX-Inspired Features

### 24/7 AI Development Team

Inspired by MGX's "Dream, Chat, Create" philosophy, our system now includes a specialized AI team:

- **👨‍💼 Mike** - Team Leader (Project coordination, strategic planning)
- **👨‍💻 Alex** - Engineer (Full-stack development, DevOps)
- **👩‍💼 Emma** - Product Manager (UX research, feature planning)
- **👨‍🔬 David** - Data Analyst (ML, analytics, visualization)
- **👨‍🏗️ Bob** - Architect (System design, scalability)
- **👩‍🎨 Sophia** - UI Designer (Interface design, prototyping)

### Team Collaboration Features

- **Project Creation**: Team analyzes requirements and assigns appropriate members
- **Multi-Agent Discussions**: Specialized agents contribute their expertise
- **Code Generation**: Team creates artifacts and components
- **Project Management**: Track progress and manage workflows

## 🌟 주요 기능

- **A2A 프로토콜 완전 호환**: Google A2A 표준 사양을 완전히 구현
- **다중 AI 모델 지원**: OpenAI, Anthropic, Google, Cohere 등 여러 AI 서비스 통합
- **유연한 스킬 시스템**: 쉽게 확장 가능한 모듈형 스킬 아키텍처
- **RESTful API**: 표준 HTTP/JSON-RPC 2.0 기반 인터페이스
- **실시간 스트리밍**: Server-Sent Events를 통한 실시간 응답
- **보안**: 표준 웹 인증 방식 지원 (API Key, Bearer Token)

## 📋 시스템 요구사항

- Python 3.8+
- FastAPI, uvicorn
- requests, aiohttp
- python-dotenv
- AI 서비스 API 키 (선택사항)

## 🚀 빠른 시작

### Installing via Smithery

To install A2A Agent System with MGX-Inspired Team Collaboration for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@Hwani-Net/a2a-agent-system):

```bash
npx -y @smithery/cli install @Hwani-Net/a2a-agent-system --client claude
```

### 1. 환경 설정

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 설정 (대화형)
python setup_env.py
```

### 2. API 키 설정

설정 스크립트를 실행하면 다음 API 키들을 입력할 수 있습니다:

- **OpenAI API Key**: 텍스트 생성 및 분석 기능용
- **Anthropic API Key**: Claude 모델 사용용 (선택사항)
- **Google API Key**: Gemini 모델 사용용 (선택사항)
- **Cohere API Key**: Cohere 모델 사용용 (선택사항)
- **Weather API Key**: 날씨 정보 기능용 (선택사항)

### 3. 서버 실행

```bash
# A2A 에이전트 서버 시작
python run_server.py
```

서버가 시작되면 다음 URL에서 접근할 수 있습니다:

- **Agent Card**: <http://localhost:8000/agent-card>
- **A2A 엔드포인트**: <http://localhost:8000/a2a>
- **Health Check**: <http://localhost:8000/health>
- **스킬 목록**: <http://localhost:8000/skills>

### 4. 클라이언트 테스트

```bash
# 클라이언트로 에이전트 테스트
python a2a_client.py
```

## 📖 사용 예시

### Python 클라이언트 사용

```python
from a2a_client import A2AClient

# 클라이언트 생성
client = A2AClient("http://localhost:8000")

# 에이전트 정보 확인
client.print_agent_info()

# 대화하기
response = client.chat_with_agent("Hello, can you help me?")
print(response)

# 특정 스킬 실행
result = client.execute_skill("text_generation", {
    "prompt": "Write a short story about AI",
    "max_tokens": 500
})
print(result)
```

### cURL을 통한 직접 API 호출

```bash
# Agent Card 조회
curl http://localhost:8000/agent-card

# 작업 생성
curl -X POST http://localhost:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "task/create",
    "id": "1"
  }'

# 메시지 전송
curl -X POST http://localhost:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "task/message",
    "params": {
      "task_id": "your-task-id",
      "message": {
        "role": "user",
        "parts": [{"type": "text", "content": "Hello!"}]
      }
    },
    "id": "2"
  }'
```

## 🔧 설정 옵션

### 환경 변수

`.env` 파일에서 다음 설정들을 조정할 수 있습니다:

```env
# AI 서비스 API 키들
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key

# 에이전트 설정
A2A_AGENT_NAME=MyCustomAgent
A2A_AGENT_PORT=8000
A2A_AGENT_HOST=localhost
```

### 커스터마이징

#### 새로운 스킬 추가

`skills.py`에서 새로운 스킬을 추가할 수 있습니다:

```python
async def _new_skill(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """새로운 스킬 구현"""
    # 스킬 로직 구현
    return {"success": True, "result": "스킬 결과"}
```

#### Agent Card 수정

`agent_card.py`에서 에이전트의 메타데이터를 수정할 수 있습니다.

## 🌐 A2A 프로토콜 호환성

이 시스템은 A2A 프로토콜 버전 0.2.1을 완전히 구현합니다:

- ✅ JSON-RPC 2.0 over HTTP(S)
- ✅ Agent Card 사양
- ✅ 작업 생명주기 관리
- ✅ 메시지 교환
- ✅ 스킬 실행
- ✅ 스트리밍 지원 (준비됨)
- ✅ 인증 및 권한 부여

## 🔗 다른 A2A 에이전트와 연결

이 에이전트는 표준 A2A 프로토콜을 구현하므로, 다른 A2A 호환 에이전트들과 쉽게 연결할 수 있습니다:

```python
# 다른 A2A 에이전트에 연결
other_agent = A2AClient("http://other-agent:8000")

# 에이전트 체인 구성
response1 = other_agent.chat_with_agent("데이터 분석해줘")
response2 = client.chat_with_agent(f"이 결과를 요약해줘: {response1}")
```

## 📚 추가 리소스

- [A2A 프로토콜 공식 문서](https://google-a2a.github.io/A2A/)
- [A2A GitHub 저장소](https://github.com/google-a2a/A2A)
- [A2A Python SDK](https://github.com/google-a2a/a2a-python)

## 🤝 기여하기

이 프로젝트에 기여하고 싶다면:

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 라이선스

MIT 라이선스 하에 배포됩니다.

## 🔧 문제 해결

### 일반적인 문제들

**Q: 서버가 시작되지 않아요**
A: `.env` 파일이 올바르게 설정되었는지 확인하고, 포트 8000이 사용 가능한지 확인하세요.

**Q: OpenAI API 오류가 발생해요**
A: API 키가 올바른지 확인하고, 충분한 크레딧이 있는지 확인하세요.

**Q: 다른 포트를 사용하고 싶어요**
A: `.env` 파일에서 `A2A_AGENT_PORT`를 변경하거나 `python run_server.py --port 9000` 처럼 실행하세요.

더 많은 도움이 필요하면 Issue를 생성해 주세요!

## 🎯 Next Steps

1. **Enhanced UI**: Web interface for team interactions
2. **Persistent Storage**: Database for projects and artifacts  
3. **Real-time Updates**: WebSocket support for live collaboration
4. **Agent Marketplace**: Discover and integrate other A2A agents
5. **Advanced Workflows**: Complex multi-step project automation

## 🤖 Inspiration

This project draws inspiration from:

- **MGX (<https://mgx.dev/>)**: Revolutionary AI team collaboration concept
- **A2A Protocol**: Interoperable agent communication standard
- **Multi-Agent Systems**: Academic research in agent collaboration

The goal is to combine MGX's innovative team-based approach with the openness and interoperability of the A2A protocol.

---

**Ready to experience the future of AI team collaboration? Start your A2A MGX-inspired agent system today!**

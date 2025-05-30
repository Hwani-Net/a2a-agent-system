# A2A Agent System 사용 가이드

## 다른 프로젝트에서 사용하기

### 1. 설치

```bash
# Git에서 클론
git clone https://github.com/yourusername/a2a-agent-system.git
cd a2a-agent-system

# 설치 스크립트 실행
./install.sh  # Linux/Mac
# 또는
install.bat  # Windows
```

### 2. 기본 사용법

#### 비동기 버전 (권장)

```python
import asyncio
from a2a_agent_system import a2a_agent, quick_generate

# 방법 1: 컨텍스트 매니저 사용
async def main():
    async with a2a_agent() as agent:
        # 텍스트 생성
        result = await agent.generate("파이썬 코드 예시를 만들어주세요.")
        print(result)
        
        # 텍스트 분석
        analysis = await agent.analyze("분석할 텍스트입니다.")
        print(analysis)
        
        # 웹 검색
        search_results = await agent.search("최신 AI 뉴스")
        print(search_results)

# 방법 2: 편의 함수 사용
async def quick_usage():
    result = await quick_generate("안녕하세요!")
    print(result)

asyncio.run(main())
```

#### 동기 버전 (간단한 용도)

```python
from a2a_agent_system import sync_generate, sync_analyze

# 간단한 텍스트 생성
result = sync_generate("파이썬에 대해 설명해주세요.")
print(result)

# 텍스트 분석
analysis = sync_analyze("분석할 텍스트입니다.")
print(analysis)
```

### 3. 고급 사용법

```python
import asyncio
from a2a_agent_system import A2AAgent

async def advanced_usage():
    agent = A2AAgent()
    
    try:
        # 연결
        await agent.connect()
        
        # 에이전트 상태 확인
        if await agent.is_alive():
            print("에이전트 연결됨")
        
        # 사용 가능한 기능 확인
        capabilities = await agent.get_capabilities()
        print(f"기능: {[cap['name'] for cap in capabilities]}")
        
        # 서버 설정 확인
        config = await agent.get_config()
        print(f"사용 가능한 모델: {config['available_models']}")
        
        # AI 기능 사용
        result = await agent.generate(
            "코드 리뷰를 해주세요.",
            model="gpt-4",
            max_tokens=500,
            temperature=0.3
        )
        print(result)
        
    finally:
        await agent.disconnect()

asyncio.run(advanced_usage())
```

### 4. MCP 클라이언트 직접 사용

```python
import asyncio
from a2a_agent_system import MCPClient

async def direct_mcp_usage():
    client = MCPClient()
    
    try:
        await client.connect()
        
        # 도구 목록 확인
        tools = await client.list_tools()
        print(f"사용 가능한 도구: {len(tools)}개")
        
        # 도구 직접 호출
        result = await client.call_tool("generate_text", {
            "prompt": "안녕하세요!",
            "max_tokens": 100
        })
        print(result)
        
    finally:
        await client.disconnect()

asyncio.run(direct_mcp_usage())
```

## 환경 설정

### API 키 설정

`.env` 파일에 다음 API 키들을 설정하세요:

```env
# 필수 (최소 하나는 설정)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# 선택사항
GOOGLE_API_KEY=your_google_api_key
COHERE_API_KEY=your_cohere_api_key
SERPER_API_KEY=your_serper_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

### 서버 직접 실행

```bash
# MCP 서버 시작
python -m a2a_agent_system.mcp_server

# 또는 기존 A2A 서버 (HTTP)
python -m a2a_agent_system.a2a_server
```

## 문제해결

### 일반적인 오류

1. **연결 실패**: API 키가 올바르게 설정되었는지 확인
2. **모듈을 찾을 수 없음**: `pip install -e .`로 재설치
3. **권한 오류**: 가상환경 사용 권장

### 로그 확인

```python
import logging
logging.basicConfig(level=logging.INFO)
```

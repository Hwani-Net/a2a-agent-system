# A2A Agent System - Smithery MCP 배포 요약

## 🔍 조사 결과

### Smithery란?

**Smithery**는 MCP (Model Context Protocol) 서버를 쉽게 배포하고 관리할 수 있는 플랫폼입니다.

#### 주요 특징

- **Docker 기반 배포**: 컨테이너화된 MCP 서버 배포
- **환경 변수 관리**: API 키를 안전하게 시크릿으로 관리
- **자동 스케일링**: 필요에 따른 서버 확장
- **모니터링**: 실시간 서버 상태 및 로그 확인
- **Version Control**: Git 기반 자동 배포

### 🔐 보안 원칙

#### ✅ 안전한 API 키 처리 방법

1. **환경 변수 사용**: 코드에 API 키 하드코딩 금지
2. **Smithery 시크릿 관리**: 배포 시 안전한 키 주입
3. **Docker 이미지 보호**: `.dockerignore`로 민감한 파일 제외
4. **로깅 방지**: API 키 값 로그 출력 차단

#### ❌ 피해야 할 것들

- API 키를 코드에 직접 작성
- `.env` 파일을 Git에 커밋
- Docker 이미지에 시크릿 포함
- 로그에 API 키 노출

## 📦 배포 구성 요소

### 생성된 파일들

1. **`Dockerfile`**
   - Python 3.11 기반
   - 비특권 사용자(`mcpuser`) 설정
   - 환경 변수로 API 키 처리

2. **`.dockerignore`**
   - `.env` 파일 제외
   - 캐시 및 빌드 아티팩트 제외
   - 개발 파일들 제외

3. **`smithery.json`**
   - MCP 서버 메타데이터
   - 환경 변수 정의 (API 키들)
   - 보안 설정

4. **`config_secure.py`**
   - 보안 강화된 설정 클래스
   - API 키 안전 검증 메서드
   - 민감한 정보 제외 설정

5. **`validate_deployment.py`**
   - 배포 전 검증 스크립트
   - 보안 설정 확인
   - Docker 구성 검증

6. **`README_SMITHERY.md`**
   - 상세한 배포 가이드
   - 사용법 및 문제 해결

## 🚀 배포 프로세스

### 1단계: 준비

```bash
# 필수 파일들 확인
python validate_deployment.py

# Git 저장소 설정
git add .
git commit -m "Add Smithery MCP deployment configuration"
git push origin main
```

### 2단계: Smithery 배포

1. **Smithery.ai** 접속
2. **새 MCP 서버 생성**
3. **GitHub 저장소 연결**
4. **환경 변수 설정**:

   ```
   OPENAI_API_KEY=sk-proj-xxx...
   ANTHROPIC_API_KEY=sk-ant-xxx...
   PERPLEXITY_API_KEY=pplx-xxx...
   SERPER_API_KEY=xxx...
   OPENWEATHER_API_KEY=xxx...
   ```

5. **배포 실행**

### 3단계: MCP 클라이언트 연결

Claude Desktop 설정:

```json
{
  "mcpServers": {
    "a2a-agent-system": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "smithery.ai/your-username/a2a-mcp-server:latest"
      ]
    }
  }
}
```

## 🛠 제공되는 도구들

### 1. 텍스트 생성 (`generate_text`)

- **요구사항**: `OPENAI_API_KEY` 또는 `ANTHROPIC_API_KEY`
- **기능**: AI 모델을 사용한 텍스트 생성

### 2. 텍스트 분석 (`analyze_text`)

- **요구사항**: AI API 키
- **기능**: 감정 분석, 요약, 인사이트 추출

### 3. 웹 검색 (`web_search`)

- **요구사항**: `PERPLEXITY_API_KEY` 또는 `SERPER_API_KEY`
- **기능**: 실시간 웹 검색

### 4. 날씨 정보 (`get_weather`)

- **요구사항**: `OPENWEATHER_API_KEY`
- **기능**: 위치별 날씨 정보

## 🔧 A2A 호환성

### A2A 프로토콜 지원

- **Agent Card**: A2A 표준 에이전트 메타데이터
- **JSON-RPC 2.0**: A2A 통신 프로토콜
- **Task Management**: 작업 생성, 관리, 완료
- **Multi-modal**: 텍스트, 파일, 구조화된 데이터

### MCP와의 차이점

- **MCP**: 도구 및 리소스 접근에 중점
- **A2A**: 에이전트 간 협업에 중점
- **통합**: MCP 도구를 사용하는 A2A 에이전트

## 📊 모니터링 및 관리

### 상태 확인

```python
# 에이전트 카드 조회
agent_card = await mcp_client.read_resource("agent://card")

# 서버 상태 확인
status = await mcp_client.read_resource("agent://status")

# 설정 정보 (민감한 정보 제외)
config = await mcp_client.read_resource("agent://config")
```

### 로그 분석

```bash
# Smithery 로그
smithery logs a2a-mcp-server

# Docker 로그
docker logs -f container-name
```

## 🔄 업데이트 전략

### 버전 관리

```bash
# 새 버전 태그
git tag v1.1.0
git push origin --tags

# Smithery 배포
smithery deploy --tag v1.1.0
```

### 롤백

```bash
# 이전 버전으로 롤백
smithery rollback a2a-mcp-server --to-version v1.0.0
```

## ⚠️ 주의사항

### 보안

1. **API 키는 절대 코드에 하드코딩하지 않기**
2. **`.env` 파일을 Git에 커밋하지 않기**
3. **정기적인 API 키 로테이션**
4. **최소 권한 원칙 적용**

### 운영

1. **정기적인 모니터링**
2. **로그 분석 및 알림 설정**
3. **백업 및 재해 복구 계획**
4. **성능 최적화**

## 🎯 배포 체크리스트

### 배포 전 확인사항

- [ ] `validate_deployment.py` 실행 통과
- [ ] 모든 필수 파일 존재
- [ ] `.gitignore`에 민감한 파일 패턴 추가
- [ ] API 키 하드코딩 없음
- [ ] Docker 빌드 테스트 완료

### 배포 후 확인사항

- [ ] Smithery 대시보드에서 서버 상태 확인
- [ ] MCP 클라이언트 연결 테스트
- [ ] 각 도구 기능 테스트
- [ ] 로그 확인 및 오류 없음
- [ ] 성능 메트릭 정상

## 📚 관련 리소스

- [Smithery 공식 문서](https://smithery.ai/docs/)
- [MCP 사양](https://modelcontextprotocol.io/)
- [A2A 프로토콜](https://a2a.to/)
- [Docker 보안 가이드](https://docs.docker.com/engine/security/)

## 🤝 지원 및 문의

문제 발생 시:

1. GitHub Issues에 문제 보고
2. Smithery 지원팀 문의
3. A2A 커뮤니티 포럼 참여

---

**결론**: 이제 A2A 에이전트 시스템을 Smithery를 통해 안전하고 효율적으로 MCP 서버로 배포할 수 있습니다. API 키는 Smithery의 시크릿 관리 시스템을 통해 안전하게 처리되며, Docker 컨테이너화를 통해 격리된 환경에서 실행됩니다.

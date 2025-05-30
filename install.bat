@echo off
echo 🚀 A2A Agent System 설치 시작...

REM 가상환경 생성 여부 확인
set /p create_venv="가상환경을 생성하시겠습니까? (y/n): "
if /i "%create_venv%"=="y" (
    echo 📦 가상환경 생성 중...
    python -m venv a2a_env
    call a2a_env\Scripts\activate.bat
    echo ✅ 가상환경 활성화 완료
)

REM 패키지 설치
echo 📥 A2A Agent System 설치 중...
pip install -e .

REM 환경변수 설정 파일 생성
if not exist .env (
    echo 🔧 환경변수 설정 파일 생성 중...
    (
        echo # AI API Keys
        echo OPENAI_API_KEY=your_openai_api_key
        echo ANTHROPIC_API_KEY=your_anthropic_api_key
        echo GOOGLE_API_KEY=your_google_api_key
        echo COHERE_API_KEY=your_cohere_api_key
        echo.
        echo # 웹 검색 API
        echo SERPER_API_KEY=your_serper_api_key_here
        echo.
        echo # 날씨 API
        echo OPENWEATHER_API_KEY=your_openweather_api_key_here
        echo.
        echo # 서버 설정
        echo A2A_SERVER_HOST=localhost
        echo A2A_SERVER_PORT=8000
        echo A2A_LOG_LEVEL=INFO
    ) > .env
    echo ✅ .env 파일 생성 완료 ^(API 키를 설정해주세요^)
)

echo 🎉 A2A Agent System 설치 완료!
echo.
echo 📋 다음 단계:
echo 1. .env 파일에 API 키를 설정하세요
echo 2. 'python -m a2a_agent_system.mcp_server' 명령어로 서버를 시작하세요
echo 3. 다른 터미널에서 'python -m a2a_agent_system.mcp_client' 명령어로 테스트하세요
pause

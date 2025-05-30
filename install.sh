#!/bin/bash
# A2A Agent System 설치 스크립트

echo "🚀 A2A Agent System 설치 시작..."

# Python 가상환경 생성 (선택사항)
read -p "가상환경을 생성하시겠습니까? (y/n): " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "📦 가상환경 생성 중..."
    python -m venv a2a_env
    
    # 운영체제별 활성화 명령어
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        source a2a_env/Scripts/activate
    else
        source a2a_env/bin/activate
    fi
    echo "✅ 가상환경 활성화 완료"
fi

# 패키지 설치
echo "📥 A2A Agent System 설치 중..."
pip install -e .

# 환경변수 설정 파일 생성
if [ ! -f .env ]; then
    echo "🔧 환경변수 설정 파일 생성 중..."
    cat > .env << EOF
# AI API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key
COHERE_API_KEY=your_cohere_api_key

# 웹 검색 API
SERPER_API_KEY=your_serper_api_key_here

# 날씨 API
OPENWEATHER_API_KEY=your_openweather_api_key_here

# 서버 설정
A2A_SERVER_HOST=localhost
A2A_SERVER_PORT=8000
A2A_LOG_LEVEL=INFO
EOF
    echo "✅ .env 파일 생성 완료 (API 키를 설정해주세요)"
fi

echo "🎉 A2A Agent System 설치 완료!"
echo ""
echo "📋 다음 단계:"
echo "1. .env 파일에 API 키를 설정하세요"
echo "2. 'python -m a2a_agent_system.mcp_server' 명령어로 서버를 시작하세요"
echo "3. 다른 터미널에서 'python -m a2a_agent_system.mcp_client' 명령어로 테스트하세요"

#!/usr/bin/env python3
"""
A2A Agent System 배포 스크립트
Git 저장소 배포 및 설치 자동화
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
from datetime import datetime


class A2ADeployer:
    """A2A 시스템 배포 관리자"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.version = "1.0.0"
        
    def run_command(self, command: str, cwd: str = None) -> tuple:
        """명령어 실행"""
        try:
            # Git 커밋 같은 복잡한 명령어는 shell=True 사용
            if "git commit" in command:
                result = subprocess.run(
                    command,
                    cwd=cwd or self.project_dir,
                    capture_output=True,
                    text=True,
                    check=True,
                    shell=True  # shell=True로 실행
                )
            else:
                result = subprocess.run(
                    command.split(),
                    cwd=cwd or self.project_dir,
                    capture_output=True,
                    text=True,
                    check=True
                )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, e.stderr.strip()
    
    def check_prerequisites(self) -> bool:
        """배포 전 필수 조건 확인"""
        print("🔍 배포 전 검사 중...")
        
        # Git 설치 확인
        success, output = self.run_command("git --version")
        if not success:
            print("❌ Git이 설치되지 않았습니다.")
            return False
        print(f"✅ Git 확인: {output}")
        
        # Python 패키지 확인
        required_files = [
            "setup.py",
            "requirements.txt",
            "README.md",
            "config.py",
            "skills.py",
            "mcp_server.py",
            "mcp_client.py"
        ]
        
        for file in required_files:
            if not (self.project_dir / file).exists():
                print(f"❌ 필수 파일 누락: {file}")
                return False
        
        print("✅ 필수 파일 확인 완료")
        return True
    
    def create_package_structure(self) -> bool:
        """패키지 구조 생성"""
        print("📦 패키지 구조 생성 중...")
        
        # __init__.py 파일 생성
        init_content = '''"""
A2A Agent System
A2A (Agent2Agent) 호환 AI 에이전트 시스템

MCP (Model Context Protocol) 서버로 동작하여
다른 프로젝트에서 재사용 가능한 AI 에이전트 기능을 제공합니다.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .mcp_client import MCPClient
from .a2a_mcp_wrapper import A2AAgent, a2a_agent, quick_generate, quick_analyze, quick_search
from .config import Config
from .skills import SkillManager

__all__ = [
    "MCPClient",
    "A2AAgent", 
    "a2a_agent",
    "quick_generate",
    "quick_analyze", 
    "quick_search",
    "Config",
    "SkillManager"
]
'''
        
        init_file = self.project_dir / "__init__.py"
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(init_content)
        
        print("✅ __init__.py 생성 완료")
        return True
    
    def create_installation_script(self) -> bool:
        """설치 스크립트 생성"""
        print("📜 설치 스크립트 생성 중...")
        
        install_script = '''#!/bin/bash
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
'''
        
        install_file = self.project_dir / "install.sh"
        with open(install_file, 'w', encoding='utf-8') as f:
            f.write(install_script)
        
        # 실행 권한 부여 (Unix 계열)
        if os.name != 'nt':
            os.chmod(install_file, 0o755)
        
        print("✅ install.sh 생성 완료")
        
        # Windows용 배치 파일도 생성
        windows_script = '''@echo off
echo 🚀 A2A Agent System 설치 시작...

REM 가상환경 생성 여부 확인
set /p create_venv="가상환경을 생성하시겠습니까? (y/n): "
if /i "%create_venv%"=="y" (
    echo 📦 가상환경 생성 중...
    python -m venv a2a_env
    call a2a_env\\Scripts\\activate.bat
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
'''
        
        windows_file = self.project_dir / "install.bat"
        with open(windows_file, 'w', encoding='utf-8') as f:
            f.write(windows_script)
        
        print("✅ install.bat 생성 완료")
        return True
    
    def create_usage_guide(self) -> bool:
        """사용 가이드 생성"""
        print("📚 사용 가이드 생성 중...")
        
        guide_content = '''# A2A Agent System 사용 가이드

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
'''
        
        guide_file = self.project_dir / "USAGE.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print("✅ USAGE.md 생성 완료")
        return True
    
    def init_git_repo(self) -> bool:
        """Git 저장소 초기화"""
        print("🔧 Git 저장소 설정 중...")
        
        # .gitignore 생성
        gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 환경변수
.env
.env.local
.env.*.local

# 가상환경
venv/
env/
ENV/
a2a_env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 로그
*.log
logs/

# 테스트
.coverage
.pytest_cache/
.tox/

# 운영체제
.DS_Store
Thumbs.db

# 임시 파일
*.tmp
*.temp
'''
        
        gitignore_file = self.project_dir / ".gitignore"
        with open(gitignore_file, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        # Git 저장소 초기화 (이미 존재하지 않는 경우)
        if not (self.project_dir / ".git").exists():
            success, output = self.run_command("git init")
            if not success:
                print(f"❌ Git 초기화 실패: {output}")
                return False
            print("✅ Git 저장소 초기화 완료")
        
        # 파일 추가
        success, output = self.run_command("git add .")
        if not success:
            print(f"❌ Git 파일 추가 실패: {output}")
            return False
        
        # 커밋
        commit_message = f"Initial deployment of A2A Agent System v{self.version}"
        success, output = self.run_command(f'git commit -m "{commit_message}"')
        if not success and "nothing to commit" not in output:
            print(f"❌ Git 커밋 실패: {output}")
            return False
        
        print("✅ Git 설정 완료")
        return True
    
    def create_release_info(self) -> bool:
        """릴리스 정보 생성"""
        print("📋 릴리스 정보 생성 중...")
        
        release_info = {
            "version": self.version,
            "release_date": datetime.now().isoformat(),
            "description": "A2A (Agent2Agent) 호환 AI 에이전트 시스템",
            "features": [
                "MCP (Model Context Protocol) 서버 지원",
                "다중 AI 모델 지원 (OpenAI, Anthropic, Google, Cohere)",
                "웹 검색 및 날씨 정보 제공",
                "비동기 및 동기 API 지원",
                "쉬운 설치 및 사용"
            ],
            "installation": {
                "git": "git clone https://github.com/yourusername/a2a-agent-system.git",
                "install": "./install.sh 또는 install.bat",
                "pip": "pip install -e ."
            },
            "requirements": [
                "Python 3.8+",
                "API 키 (최소 하나의 AI 서비스)"
            ]
        }
        
        release_file = self.project_dir / "RELEASE.json"
        with open(release_file, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, ensure_ascii=False, indent=2)
        
        print("✅ RELEASE.json 생성 완료")
        return True
    
    def deploy(self) -> bool:
        """전체 배포 프로세스 실행"""
        print("🚀 A2A Agent System 배포 시작\n")
        
        steps = [
            ("전제조건 확인", self.check_prerequisites),
            ("패키지 구조 생성", self.create_package_structure),
            ("설치 스크립트 생성", self.create_installation_script),
            ("사용 가이드 생성", self.create_usage_guide),
            ("Git 저장소 설정", self.init_git_repo),
            ("릴리스 정보 생성", self.create_release_info)
        ]
        
        for step_name, step_func in steps:
            print(f"\n--- {step_name} ---")
            if not step_func():
                print(f"❌ {step_name} 실패")
                return False
            print(f"✅ {step_name} 완료")
        
        print("\n🎉 배포 완료!")
        print("\n📋 다음 단계:")
        print("1. GitHub에 저장소를 생성하세요")
        print("2. 'git remote add origin <repository-url>' 명령어로 원격 저장소를 추가하세요")
        print("3. 'git push -u origin main' 명령어로 코드를 푸시하세요")
        print("4. 다른 프로젝트에서 Git URL로 설치하여 사용하세요")
        
        return True


def main():
    """메인 함수"""
    deployer = A2ADeployer()
    
    try:
        success = deployer.deploy()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ 배포가 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 배포 중 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
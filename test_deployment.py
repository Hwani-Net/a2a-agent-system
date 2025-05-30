#!/usr/bin/env python3
"""
A2A Agent System 배포 테스트
"""

import os
import sys
import json
import importlib.util
from pathlib import Path

def test_files_exist():
    """필수 파일 존재 확인"""
    print("📁 필수 파일 존재 확인...")
    
    required_files = [
        "__init__.py",
        "setup.py", 
        "mcp_server.py",
        "mcp_client.py",
        "a2a_mcp_wrapper.py",
        "mcp_config.json",
        "install.sh",
        "install.bat",
        "USAGE.md",
        "RELEASE.json",
        ".gitignore"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"  ✅ {file}")
    
    if missing_files:
        print(f"  ❌ 누락된 파일: {missing_files}")
        return False
    
    print("✅ 모든 필수 파일 존재함")
    return True

def test_package_structure():
    """패키지 구조 확인"""
    print("\n📦 패키지 구조 확인...")
    
    try:
        # __init__.py 내용 확인
        with open("__init__.py", 'r', encoding='utf-8') as f:
            init_content = f.read()
            
        if "__version__" in init_content and "__all__" in init_content:
            print("  ✅ __init__.py 구조 올바름")
        else:
            print("  ❌ __init__.py 구조 문제")
            return False
            
        # setup.py 구조 확인
        spec = importlib.util.spec_from_file_location("setup", "setup.py")
        if spec:
            print("  ✅ setup.py 구조 올바름")
        else:
            print("  ❌ setup.py 구조 문제")
            return False
            
        print("✅ 패키지 구조 올바름")
        return True
        
    except Exception as e:
        print(f"  ❌ 패키지 구조 확인 실패: {e}")
        return False

def test_mcp_config():
    """MCP 설정 파일 확인"""
    print("\n⚙️ MCP 설정 확인...")
    
    try:
        with open("mcp_config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 필수 섹션 확인
        required_sections = ["mcpServers", "defaults", "global"]
        for section in required_sections:
            if section not in config:
                print(f"  ❌ 누락된 섹션: {section}")
                return False
            print(f"  ✅ {section} 섹션 존재")
        
        # A2A 서버 설정 확인
        if "a2a-agent-system" in config["mcpServers"]:
            server_config = config["mcpServers"]["a2a-agent-system"]
            if all(key in server_config for key in ["command", "args", "capabilities"]):
                print("  ✅ A2A 서버 설정 올바름")
            else:
                print("  ❌ A2A 서버 설정 불완전")
                return False
        else:
            print("  ❌ A2A 서버 설정 누락")
            return False
        
        print("✅ MCP 설정 올바름")
        return True
        
    except Exception as e:
        print(f"  ❌ MCP 설정 확인 실패: {e}")
        return False

def test_release_info():
    """릴리스 정보 확인"""
    print("\n📋 릴리스 정보 확인...")
    
    try:
        with open("RELEASE.json", 'r', encoding='utf-8') as f:
            release = json.load(f)
        
        required_fields = ["version", "release_date", "description", "features", "installation"]
        for field in required_fields:
            if field not in release:
                print(f"  ❌ 누락된 필드: {field}")
                return False
            print(f"  ✅ {field} 필드 존재")
        
        print(f"  📌 버전: {release['version']}")
        print(f"  📌 기능 수: {len(release['features'])}개")
        
        print("✅ 릴리스 정보 올바름")
        return True
        
    except Exception as e:
        print(f"  ❌ 릴리스 정보 확인 실패: {e}")
        return False

def test_documentation():
    """문서 확인"""
    print("\n📚 문서 확인...")
    
    try:
        # USAGE.md 확인
        with open("USAGE.md", 'r', encoding='utf-8') as f:
            usage_content = f.read()
        
        if len(usage_content) > 1000 and "사용 가이드" in usage_content:
            print("  ✅ USAGE.md 문서 올바름")
        else:
            print("  ❌ USAGE.md 문서 불완전")
            return False
        
        # 설치 스크립트 확인
        install_scripts = ["install.sh", "install.bat"]
        for script in install_scripts:
            if Path(script).exists() and Path(script).stat().st_size > 100:
                print(f"  ✅ {script} 존재함")
            else:
                print(f"  ❌ {script} 문제")
                return False
        
        print("✅ 문서 및 스크립트 올바름")
        return True
        
    except Exception as e:
        print(f"  ❌ 문서 확인 실패: {e}")
        return False

def test_git_setup():
    """Git 설정 확인"""
    print("\n🔧 Git 설정 확인...")
    
    try:
        # .git 디렉토리 존재 확인
        if Path(".git").exists():
            print("  ✅ Git 저장소 초기화됨")
        else:
            print("  ❌ Git 저장소 없음")
            return False
        
        # .gitignore 확인
        if Path(".gitignore").exists():
            with open(".gitignore", 'r', encoding='utf-8') as f:
                gitignore_content = f.read()
            
            if "__pycache__" in gitignore_content and ".env" in gitignore_content:
                print("  ✅ .gitignore 설정 올바름")
            else:
                print("  ❌ .gitignore 설정 불완전")
                return False
        else:
            print("  ❌ .gitignore 파일 없음")
            return False
        
        print("✅ Git 설정 올바름")
        return True
        
    except Exception as e:
        print(f"  ❌ Git 설정 확인 실패: {e}")
        return False

def show_deployment_summary():
    """배포 요약 정보 표시"""
    print("\n" + "="*60)
    print("🎉 A2A Agent System MCP 배포 요약")
    print("="*60)
    
    try:
        # 릴리스 정보 표시
        with open("RELEASE.json", 'r', encoding='utf-8') as f:
            release = json.load(f)
        
        print(f"📦 패키지: {release['description']}")
        print(f"🏷️  버전: {release['version']}")
        print(f"📅 릴리스 날짜: {release['release_date']}")
        
        print(f"\n✨ 주요 기능:")
        for i, feature in enumerate(release['features'], 1):
            print(f"   {i}. {feature}")
        
        print(f"\n🛠️ 설치 방법:")
        print(f"   Git: {release['installation']['git']}")
        print(f"   설치: {release['installation']['install']}")
        print(f"   Pip: {release['installation']['pip']}")
        
        print(f"\n📋 다음 단계:")
        print("   1. GitHub 저장소 생성")
        print("   2. 원격 저장소 추가: git remote add origin <repo-url>")
        print("   3. 코드 푸시: git push -u origin main")
        print("   4. 다른 프로젝트에서 git clone으로 설치")
        
    except Exception as e:
        print(f"요약 정보 표시 실패: {e}")

def main():
    """테스트 실행"""
    print("🧪 A2A Agent System 배포 테스트 시작")
    print("="*50)
    
    tests = [
        ("파일 존재 확인", test_files_exist),
        ("패키지 구조 확인", test_package_structure),
        ("MCP 설정 확인", test_mcp_config),
        ("릴리스 정보 확인", test_release_info),
        ("문서 확인", test_documentation),
        ("Git 설정 확인", test_git_setup)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 실패")
        except Exception as e:
            print(f"❌ {test_name} 오류: {e}")
    
    print(f"\n📊 테스트 결과: {passed}/{total} 통과")
    
    if passed == total:
        print("🎉 모든 테스트 통과! 배포 준비 완료!")
        show_deployment_summary()
        return True
    else:
        print("❌ 일부 테스트 실패")
        return False

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Smithery MCP Deployment Validation Script
A2A 에이전트 시스템의 Smithery 배포 전 검증 도구
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import subprocess
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class DeploymentValidator:
    """Smithery MCP 배포 검증 클래스"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.current_dir = Path.cwd()
        
    def validate_all(self) -> bool:
        """모든 검증 단계 실행"""
        logger.info("🔍 Smithery MCP 배포 준비 상태 검증 중...")
        
        # 필수 파일들 확인
        self.validate_required_files()
        
        # Smithery 설정 검증
        self.validate_smithery_config()
        
        # Docker 설정 검증
        self.validate_docker_config()
        
        # 보안 설정 검증
        self.validate_security_config()
        
        # Python 의존성 검증
        self.validate_dependencies()
        
        # 코드 구조 검증
        self.validate_code_structure()
        
        # 결과 리포트 출력
        return self.generate_report()
    
    def validate_required_files(self):
        """필수 파일들이 존재하는지 확인"""
        logger.info("📁 필수 파일 확인 중...")
        
        required_files = [
            "Dockerfile",
            ".dockerignore", 
            "smithery.json",
            "requirements.txt",
            "mcp_server.py",
            "config_secure.py"
        ]
        
        for file_name in required_files:
            file_path = self.current_dir / file_name
            if not file_path.exists():
                self.errors.append(f"필수 파일 누락: {file_name}")
            else:
                logger.info(f"  ✅ {file_name}")
    
    def validate_smithery_config(self):
        """smithery.json 설정 검증"""
        logger.info("⚙️ Smithery 설정 검증 중...")
        
        smithery_file = self.current_dir / "smithery.json"
        if not smithery_file.exists():
            self.errors.append("smithery.json 파일이 없습니다")
            return
        
        try:
            with open(smithery_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 필수 필드 확인
            required_fields = ["name", "version", "description", "type", "capabilities"]
            for field in required_fields:
                if field not in config:
                    self.errors.append(f"smithery.json에서 필수 필드 누락: {field}")
                else:
                    logger.info(f"  ✅ {field}: {config.get(field, 'N/A')}")
            
            # 환경 변수 설정 확인
            if "environment" in config:
                env_config = config["environment"]
                if "optional" in env_config:
                    api_keys = [item["name"] for item in env_config["optional"] if item.get("type") == "secret"]
                    logger.info(f"  ✅ API 키 환경 변수들: {', '.join(api_keys)}")
                else:
                    self.warnings.append("환경 변수 설정이 없습니다")
            
            # 보안 설정 확인
            if "security" in config:
                security = config["security"]
                if security.get("apiKeysHandling") == "environment-variables":
                    logger.info("  ✅ API 키 보안 처리: environment-variables")
                else:
                    self.warnings.append("API 키 보안 처리 방식이 명시되지 않았습니다")
            
        except json.JSONDecodeError as e:
            self.errors.append(f"smithery.json 파싱 오류: {e}")
        except Exception as e:
            self.errors.append(f"smithery.json 검증 오류: {e}")
    
    def validate_docker_config(self):
        """Docker 설정 검증"""
        logger.info("🐳 Docker 설정 검증 중...")
        
        # Dockerfile 검증
        dockerfile = self.current_dir / "Dockerfile"
        if dockerfile.exists():
            with open(dockerfile, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 보안 관련 검증
            if "USER mcpuser" in content:
                logger.info("  ✅ 비특권 사용자 설정")
            else:
                self.warnings.append("Docker에서 root 사용자로 실행됩니다 (보안 위험)")
            
            if "COPY . ." in content and ".dockerignore" in content:
                logger.info("  ✅ .dockerignore 사용")
            
            if "ENTRYPOINT" in content:
                logger.info("  ✅ ENTRYPOINT 설정")
        
        # .dockerignore 검증
        dockerignore = self.current_dir / ".dockerignore"
        if dockerignore.exists():
            with open(dockerignore, 'r', encoding='utf-8') as f:
                ignore_content = f.read()
            
            # 민감한 파일들이 제외되는지 확인
            sensitive_patterns = [".env", "*.env", ".git", "__pycache__", "*.pyc"]
            for pattern in sensitive_patterns:
                if pattern in ignore_content:
                    logger.info(f"  ✅ {pattern} 제외")
                else:
                    self.warnings.append(f"{pattern} 파일들이 Docker 이미지에 포함될 수 있습니다")
    
    def validate_security_config(self):
        """보안 설정 검증"""
        logger.info("🔐 보안 설정 검증 중...")
        
        # config_secure.py 검증
        secure_config = self.current_dir / "config_secure.py"
        if secure_config.exists():
            with open(secure_config, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # API 키 하드코딩 검증
            if "sk-" in content and "getenv" not in content:
                self.errors.append("config_secure.py에 API 키가 하드코딩된 것 같습니다")
            else:
                logger.info("  ✅ API 키 하드코딩 없음")
            
            # 환경 변수 사용 확인
            if "os.getenv" in content:
                logger.info("  ✅ 환경 변수 사용")
            
            # 보안 메서드 존재 확인
            if "is_api_key_available" in content:
                logger.info("  ✅ 안전한 API 키 검증 메서드")
            
            if "get_sanitized_config" in content:
                logger.info("  ✅ 민감한 정보 제외 설정 메서드")
        
        # .env 파일이 있는지 확인 (있으면 안 됨)
        env_files = list(self.current_dir.glob(".env*"))
        if env_files:
            self.warnings.append(f"환경 파일들이 발견되었습니다: {[f.name for f in env_files]}. 이 파일들은 Git에 커밋하지 마세요!")
    
    def validate_dependencies(self):
        """Python 의존성 검증"""
        logger.info("📦 Python 의존성 검증 중...")
        
        requirements_file = self.current_dir / "requirements.txt"
        if requirements_file.exists():
            with open(requirements_file, 'r', encoding='utf-8') as f:
                requirements = f.read().strip().split('\n')
            
            # 필수 의존성 확인
            required_packages = ["fastapi", "openai", "anthropic", "python-dotenv"]
            found_packages = []
            
            for req in requirements:
                package_name = req.split('==')[0].split('>=')[0].split('<=')[0].strip()
                if package_name in required_packages:
                    found_packages.append(package_name)
                    logger.info(f"  ✅ {req}")
            
            missing = set(required_packages) - set(found_packages)
            if missing:
                self.warnings.append(f"권장 패키지 누락: {', '.join(missing)}")
        else:
            self.errors.append("requirements.txt 파일이 없습니다")
    
    def validate_code_structure(self):
        """코드 구조 검증"""
        logger.info("🏗️ 코드 구조 검증 중...")
        
        # MCP 서버 파일 확인
        mcp_server = self.current_dir / "mcp_server.py"
        if mcp_server.exists():
            with open(mcp_server, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # MCP 필수 메서드 확인
            required_methods = ["initialize", "tools/list", "tools/call"]
            for method in required_methods:
                if method in content:
                    logger.info(f"  ✅ MCP 메서드: {method}")
                else:
                    self.warnings.append(f"MCP 메서드 누락: {method}")
        
        # 기타 필수 모듈 확인
        modules = ["skills.py", "agent_card.py"]
        for module in modules:
            if (self.current_dir / module).exists():
                logger.info(f"  ✅ 모듈: {module}")
            else:
                self.warnings.append(f"모듈 누락: {module}")
    
    def check_git_status(self):
        """Git 상태 확인"""
        logger.info("📝 Git 상태 확인 중...")
        
        try:
            # .gitignore 확인
            gitignore = self.current_dir / ".gitignore"
            if gitignore.exists():
                with open(gitignore, 'r', encoding='utf-8') as f:
                    ignore_content = f.read()
                
                sensitive_patterns = [".env", "*.env", "__pycache__", "*.pyc"]
                for pattern in sensitive_patterns:
                    if pattern in ignore_content:
                        logger.info(f"  ✅ .gitignore에 {pattern} 포함")
                    else:
                        self.warnings.append(f".gitignore에 {pattern} 패턴 추가 권장")
            
            # Git 상태 확인
            result = subprocess.run(["git", "status", "--porcelain"], 
                                  capture_output=True, text=True, cwd=self.current_dir)
            if result.returncode == 0:
                if result.stdout.strip():
                    self.warnings.append("커밋되지 않은 변경사항이 있습니다")
                else:
                    logger.info("  ✅ 모든 변경사항이 커밋됨")
            
        except FileNotFoundError:
            self.warnings.append("Git이 설치되지 않았거나 Git 저장소가 아닙니다")
        except Exception as e:
            self.warnings.append(f"Git 상태 확인 오류: {e}")
    
    def test_docker_build(self):
        """Docker 빌드 테스트"""
        logger.info("🔨 Docker 빌드 테스트 중...")
        
        try:
            # Docker가 설치되어 있는지 확인
            result = subprocess.run(["docker", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                self.warnings.append("Docker가 설치되지 않았습니다")
                return
            
            logger.info("  ✅ Docker 설치 확인")
            
            # 빌드 테스트 (실제로는 dry-run)
            logger.info("  ℹ️ 실제 Docker 빌드는 시간이 오래 걸릴 수 있습니다")
            logger.info("  ℹ️ 수동으로 'docker build -t a2a-mcp-server .' 명령어로 테스트하세요")
            
        except FileNotFoundError:
            self.warnings.append("Docker가 설치되지 않았습니다")
        except Exception as e:
            self.warnings.append(f"Docker 확인 오류: {e}")
    
    def generate_report(self) -> bool:
        """검증 결과 리포트 생성"""
        logger.info("\n" + "="*60)
        logger.info("📋 SMITHERY MCP 배포 검증 결과")
        logger.info("="*60)
        
        if not self.errors and not self.warnings:
            logger.info("🎉 모든 검증을 통과했습니다!")
            logger.info("✅ Smithery 배포 준비 완료")
            return True
        
        if self.errors:
            logger.error(f"\n❌ 오류 ({len(self.errors)}개):")
            for i, error in enumerate(self.errors, 1):
                logger.error(f"  {i}. {error}")
        
        if self.warnings:
            logger.warning(f"\n⚠️ 경고 ({len(self.warnings)}개):")
            for i, warning in enumerate(self.warnings, 1):
                logger.warning(f"  {i}. {warning}")
        
        if self.errors:
            logger.error("\n🚫 오류를 수정한 후 다시 시도하세요.")
            return False
        else:
            logger.warning("\n⚠️ 경고사항을 검토하고 Smithery에 배포하세요.")
            return True
    
    def suggest_fixes(self):
        """수정 방법 제안"""
        if self.errors or self.warnings:
            logger.info("\n💡 수정 방법:")
            logger.info("  1. 누락된 파일들을 생성하세요")
            logger.info("  2. smithery.json 설정을 확인하세요")
            logger.info("  3. .env 파일들이 .gitignore에 포함되었는지 확인하세요")
            logger.info("  4. API 키가 코드에 하드코딩되지 않았는지 확인하세요")
            logger.info("  5. Docker 빌드가 정상적으로 되는지 테스트하세요")

def main():
    """메인 함수"""
    print("🚀 A2A Agent System - Smithery MCP 배포 검증 도구")
    print("=" * 60)
    
    validator = DeploymentValidator()
    
    # 모든 검증 실행
    success = validator.validate_all()
    
    # Git 상태 확인
    validator.check_git_status()
    
    # Docker 빌드 테스트
    validator.test_docker_build()
    
    # 최종 리포트
    success = validator.generate_report()
    
    # 수정 방법 제안
    validator.suggest_fixes()
    
    print("\n" + "="*60)
    if success:
        print("🎯 다음 단계: Smithery 대시보드에서 배포를 진행하세요!")
        print("   1. GitHub 저장소에 코드 push")
        print("   2. Smithery.ai에서 새 MCP 서버 생성")
        print("   3. 환경 변수 설정 (API 키들)")
        print("   4. 배포 실행")
    else:
        print("❌ 오류를 수정한 후 다시 검증하세요.")
        sys.exit(1)

if __name__ == "__main__":
    main() 
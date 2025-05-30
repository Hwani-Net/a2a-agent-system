#!/usr/bin/env python3
"""
A2A Agent System Setup Script
"""

from setuptools import setup, find_packages
import os

# 현재 디렉토리
here = os.path.abspath(os.path.dirname(__file__))

# README 파일 읽기
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# requirements.txt 읽기
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="a2a-agent-system",
    version="1.0.0",
    description="A2A (Agent2Agent) 호환 AI 에이전트 시스템",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # 작성자 정보
    author="Your Name",
    author_email="your.email@example.com",
    
    # 프로젝트 URL
    url="https://github.com/yourusername/a2a-agent-system",
    
    # 패키지 정보
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.8',
    
    # 의존성
    install_requires=requirements,
    
    # 추가 의존성 그룹
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-asyncio>=0.18.0',
            'black>=22.0',
            'flake8>=4.0',
            'mypy>=0.900'
        ],
        'docs': [
            'mkdocs>=1.4.0',
            'mkdocs-material>=8.0'
        ]
    },
    
    # 패키지 데이터
    package_data={
        'a2a_agent_system': [
            'agent_card.json',
            '*.md',
            '*.txt'
        ]
    },
    include_package_data=True,
    
    # 분류자
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    
    # 엔트리 포인트 (명령행 도구)
    entry_points={
        'console_scripts': [
            'a2a-server=a2a_agent_system.mcp_server:main',
            'a2a-client=a2a_agent_system.mcp_client:example_usage',
            'a2a-setup=a2a_agent_system.setup_env:main'
        ]
    },
    
    # 키워드
    keywords="ai agent a2a mcp model-context-protocol json-rpc",
    
    # 프로젝트 URL들
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/a2a-agent-system/issues',
        'Source': 'https://github.com/yourusername/a2a-agent-system',
        'Documentation': 'https://yourusername.github.io/a2a-agent-system'
    }
) 
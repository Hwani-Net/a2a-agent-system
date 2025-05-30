"""
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

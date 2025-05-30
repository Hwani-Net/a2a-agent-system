"""
Secure Configuration for A2A Agent System MCP Deployment
Designed for production deployment via Smithery
"""
import os
import logging
from typing import Optional, Dict, Any
import warnings

# Suppress warnings about missing .env files in deployment
warnings.filterwarnings("ignore", message=".*\.env.*not found.*")

class SecureConfig:
    """
    Secure configuration class for Smithery MCP deployment
    
    This class handles API keys and configuration securely:
    - Never logs or prints API key values
    - Provides safe validation without exposing secrets
    - Uses proper environment variable naming conventions
    """
    
    # AI Service API Keys (Smithery will inject these as environment variables)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY") 
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    
    # A2A Agent Settings
    AGENT_NAME = os.getenv("A2A_AGENT_NAME", "A2A-MCP-Agent")
    AGENT_PORT = int(os.getenv("A2A_AGENT_PORT", "8000"))
    AGENT_HOST = os.getenv("A2A_AGENT_HOST", "0.0.0.0")  # Listen on all interfaces for deployment
    
    # MCP-specific settings
    MCP_MODE = os.getenv("MCP_MODE", "server")  # server or client
    MCP_TRANSPORT = os.getenv("MCP_TRANSPORT", "stdio")  # stdio or http
    
    # Agent Description
    AGENT_DESCRIPTION = "A2A (Agent2Agent) compatible AI agent system with MCP support"
    AGENT_VERSION = "1.0.0"
    
    # Deployment environment
    DEPLOYMENT_ENV = os.getenv("DEPLOYMENT_ENV", "development")  # development, staging, production
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def is_api_key_available(cls, key_name: str) -> bool:
        """
        Safely check if an API key is available without exposing its value
        
        Args:
            key_name: The name of the environment variable
            
        Returns:
            bool: True if the key exists and is not empty
        """
        key_value = getattr(cls, key_name, None)
        return key_value is not None and len(key_value.strip()) > 0
    
    @classmethod
    def get_available_capabilities(cls) -> Dict[str, Any]:
        """
        Return capabilities based on available API keys
        
        Returns:
            dict: Available capabilities configuration
        """
        capabilities = {
            "tools": [],
            "resources": [
                {
                    "uri": "agent://card",
                    "name": "Agent Card", 
                    "description": "A2A agent card information"
                },
                {
                    "uri": "agent://config",
                    "name": "Configuration",
                    "description": "Current server configuration (sanitized)"
                },
                {
                    "uri": "agent://status", 
                    "name": "Server Status",
                    "description": "Real-time server status"
                }
            ],
            "prompts": []
        }
        
        # Add tools based on available API keys
        if cls.is_api_key_available("OPENAI_API_KEY") or cls.is_api_key_available("ANTHROPIC_API_KEY"):
            capabilities["tools"].extend([
                {
                    "name": "generate_text",
                    "description": "Generate text using available AI models"
                },
                {
                    "name": "analyze_text", 
                    "description": "Analyze text for sentiment, summary, and insights"
                }
            ])
        
        if cls.is_api_key_available("PERPLEXITY_API_KEY") or cls.is_api_key_available("SERPER_API_KEY"):
            capabilities["tools"].append({
                "name": "web_search",
                "description": "Search the web for information"
            })
            
        if cls.is_api_key_available("OPENWEATHER_API_KEY"):
            capabilities["tools"].append({
                "name": "get_weather", 
                "description": "Get current weather information"
            })
        
        return capabilities
    
    @classmethod
    def validate_deployment_readiness(cls) -> Dict[str, Any]:
        """
        Validate configuration for deployment without exposing sensitive data
        
        Returns:
            dict: Validation results with status and available services
        """
        validation_result = {
            "status": "ready",
            "warnings": [],
            "available_services": [],
            "missing_services": []
        }
        
        # Check AI providers
        ai_providers = []
        if cls.is_api_key_available("OPENAI_API_KEY"):
            ai_providers.append("OpenAI")
        if cls.is_api_key_available("ANTHROPIC_API_KEY"):
            ai_providers.append("Anthropic")
            
        if ai_providers:
            validation_result["available_services"].append(f"AI Text Generation: {', '.join(ai_providers)}")
        else:
            validation_result["missing_services"].append("AI Text Generation (no OpenAI or Anthropic keys)")
            validation_result["warnings"].append("No AI providers available - text generation will be limited")
        
        # Check search providers
        search_providers = []
        if cls.is_api_key_available("PERPLEXITY_API_KEY"):
            search_providers.append("Perplexity")
        if cls.is_api_key_available("SERPER_API_KEY"):
            search_providers.append("Serper")
            
        if search_providers:
            validation_result["available_services"].append(f"Web Search: {', '.join(search_providers)}")
        else:
            validation_result["missing_services"].append("Web Search (no Perplexity or Serper keys)")
        
        # Check weather service
        if cls.is_api_key_available("OPENWEATHER_API_KEY"):
            validation_result["available_services"].append("Weather Service: OpenWeatherMap")
        else:
            validation_result["missing_services"].append("Weather Service (no OpenWeatherMap key)")
        
        # Determine overall status
        if not ai_providers:
            validation_result["status"] = "limited"
        
        return validation_result
    
    @classmethod
    def get_sanitized_config(cls) -> Dict[str, Any]:
        """
        Get configuration for logging/debugging without sensitive information
        
        Returns:
            dict: Safe configuration data
        """
        return {
            "agent_name": cls.AGENT_NAME,
            "agent_host": cls.AGENT_HOST,
            "agent_port": cls.AGENT_PORT,
            "agent_version": cls.AGENT_VERSION,
            "mcp_mode": cls.MCP_MODE,
            "mcp_transport": cls.MCP_TRANSPORT,
            "deployment_env": cls.DEPLOYMENT_ENV,
            "log_level": cls.LOG_LEVEL,
            "api_keys_status": {
                "openai": cls.is_api_key_available("OPENAI_API_KEY"),
                "anthropic": cls.is_api_key_available("ANTHROPIC_API_KEY"),
                "perplexity": cls.is_api_key_available("PERPLEXITY_API_KEY"),
                "serper": cls.is_api_key_available("SERPER_API_KEY"),
                "openweather": cls.is_api_key_available("OPENWEATHER_API_KEY")
            }
        }
    
    @classmethod
    def setup_logging(cls):
        """Setup logging for the deployment environment"""
        log_level = getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
        
        # Create logger for this module
        logger = logging.getLogger("a2a_secure_config")
        logger.info(f"Configuration loaded for deployment environment: {cls.DEPLOYMENT_ENV}")
        
        return logger

def get_openai_client():
    """Get OpenAI client instance if API key is available"""
    if SecureConfig.is_api_key_available("OPENAI_API_KEY"):
        import openai
        return openai.OpenAI(api_key=SecureConfig.OPENAI_API_KEY)
    return None

def get_anthropic_client():
    """Get Anthropic client instance if API key is available"""
    if SecureConfig.is_api_key_available("ANTHROPIC_API_KEY"):
        try:
            import anthropic
            return anthropic.Anthropic(api_key=SecureConfig.ANTHROPIC_API_KEY)
        except ImportError:
            logging.warning("Anthropic package not installed")
    return None 
"""
Configuration for the A2A Agent System
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # AI Service API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
    
    # A2A Agent Settings
    AGENT_NAME = os.getenv("A2A_AGENT_NAME", "MyCustomAgent")
    AGENT_PORT = int(os.getenv("A2A_AGENT_PORT", "8000"))
    AGENT_HOST = os.getenv("A2A_AGENT_HOST", "localhost")
    
    # Other Service API Keys
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
    
    # Agent Description
    AGENT_DESCRIPTION = "A versatile AI agent capable of text processing, web search, and multi-modal interactions"
    AGENT_VERSION = "1.0.0"
    
    @classmethod
    def validate_keys(cls):
        """Validate that required API keys are present"""
        missing_keys = []
        
        if not cls.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        
        if missing_keys:
            print(f"Warning: Missing API keys: {', '.join(missing_keys)}")
            print("Please set these in your .env file or environment variables")
        
        return len(missing_keys) == 0

def get_openai_client():
    """Get OpenAI client instance"""
    import openai
    return openai.OpenAI(api_key=Config.OPENAI_API_KEY) 
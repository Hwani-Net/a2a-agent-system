"""
Skills for the A2A Agent System
"""
from typing import Dict, List, Any, Optional
import json
import requests
import openai
from config import Config

class AgentSkills:
    def __init__(self):
        # Initialize AI clients
        if Config.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        else:
            self.openai_client = None
    
    def get_available_skills(self) -> List[Dict[str, Any]]:
        """Return list of available skills for the Agent Card"""
        skills = [
            {
                "name": "text_generation",
                "description": "Generate text using AI language models",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The text prompt to generate from"
                        },
                        "model": {
                            "type": "string",
                            "description": "AI model to use (gpt-4, gpt-3.5-turbo, etc.)",
                            "default": "gpt-3.5-turbo"
                        },
                        "max_tokens": {
                            "type": "integer",
                            "description": "Maximum tokens to generate",
                            "default": 1000
                        }
                    },
                    "required": ["prompt"]
                }
            },
            {
                "name": "text_analysis",
                "description": "Analyze and summarize text content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to analyze"
                        },
                        "analysis_type": {
                            "type": "string",
                            "description": "Type of analysis (summary, sentiment, keywords)",
                            "enum": ["summary", "sentiment", "keywords", "all"],
                            "default": "summary"
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "web_search",
                "description": "Search the web for information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "Number of results to return",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "weather_info",
                "description": "Get weather information for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Location name or coordinates"
                        }
                    },
                    "required": ["location"]
                }
            }
        ]
        
        # Filter skills based on available API keys
        available_skills = []
        for skill in skills:
            if skill["name"] in ["text_generation", "text_analysis"] and not Config.OPENAI_API_KEY:
                continue
            if skill["name"] == "weather_info" and not Config.WEATHER_API_KEY:
                continue
            available_skills.append(skill)
        
        return available_skills
    
    async def execute_skill(self, skill_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific skill with given parameters"""
        try:
            if skill_name == "text_generation":
                return await self._text_generation(parameters)
            elif skill_name == "text_analysis":
                return await self._text_analysis(parameters)
            elif skill_name == "web_search":
                return await self._web_search(parameters)
            elif skill_name == "weather_info":
                return await self._weather_info(parameters)
            else:
                return {
                    "success": False,
                    "error": f"Unknown skill: {skill_name}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error executing {skill_name}: {str(e)}"
            }
    
    async def _text_generation(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate text using OpenAI"""
        if not self.openai_client:
            return {"success": False, "error": "OpenAI API key not configured"}
        
        prompt = parameters.get("prompt")
        model = parameters.get("model", "gpt-3.5-turbo")
        max_tokens = parameters.get("max_tokens", 1000)
        
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        
        return {
            "success": True,
            "result": {
                "generated_text": response.choices[0].message.content,
                "model_used": model,
                "tokens_used": response.usage.total_tokens
            }
        }
    
    async def _text_analysis(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze text using OpenAI"""
        if not self.openai_client:
            return {"success": False, "error": "OpenAI API key not configured"}
        
        text = parameters.get("text")
        analysis_type = parameters.get("analysis_type", "summary")
        
        if analysis_type == "summary":
            prompt = f"Please provide a concise summary of the following text:\n\n{text}"
        elif analysis_type == "sentiment":
            prompt = f"Analyze the sentiment of the following text (positive, negative, neutral):\n\n{text}"
        elif analysis_type == "keywords":
            prompt = f"Extract the main keywords from the following text:\n\n{text}"
        else:  # all
            prompt = f"Provide a summary, sentiment analysis, and keywords for the following text:\n\n{text}"
        
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        return {
            "success": True,
            "result": {
                "analysis": response.choices[0].message.content,
                "analysis_type": analysis_type
            }
        }
    
    async def _web_search(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Perform web search (simplified mock implementation)"""
        query = parameters.get("query")
        num_results = parameters.get("num_results", 5)
        
        # This is a mock implementation
        # In a real implementation, you would use a search API like Google Search API
        return {
            "success": True,
            "result": {
                "query": query,
                "results": [
                    {
                        "title": f"Search result {i+1} for: {query}",
                        "url": f"https://example.com/result{i+1}",
                        "snippet": f"This is a mock search result {i+1} for the query '{query}'"
                    }
                    for i in range(num_results)
                ]
            }
        }
    
    async def _weather_info(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get weather information (mock implementation)"""
        location = parameters.get("location")
        
        # Mock weather data
        return {
            "success": True,
            "result": {
                "location": location,
                "temperature": "22°C",
                "condition": "Sunny",
                "humidity": "65%",
                "wind_speed": "15 km/h"
            }
        } 
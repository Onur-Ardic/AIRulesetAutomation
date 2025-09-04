"""
OpenAI provider implementation
"""
import openai
from typing import Dict, Any
from app.services.ai_provider import AIProvider
from app.core.config import settings

class OpenAIProvider(AIProvider):
    """OpenAI provider"""
    
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        
    async def generate_content(self, prompt: str) -> str:
        """OpenAI ile içerik üret"""
        if not settings.OPENAI_API_KEY:
            raise Exception("OpenAI API key bulunamadı")
        
        try:
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API hatası: {str(e)}")
    
    async def check_health(self) -> Dict[str, Any]:
        """OpenAI sağlık kontrolü"""
        try:
            if not settings.OPENAI_API_KEY:
                return {
                    "available": False,
                    "error": "API key eksik"
                }
            
            # Basit bir test prompt'u gönder
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            
            return {
                "available": True,
                "model": settings.OPENAI_MODEL,
                "status": "healthy"
            }
        except Exception as e:
            return {
                "available": False,
                "error": str(e)
            }
    
    @property
    def provider_name(self) -> str:
        return "openai"

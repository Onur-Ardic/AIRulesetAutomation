"""
Gemini AI provider implementation
"""
import google.generativeai as genai
from typing import Dict, Any
from app.services.ai_provider import AIProvider
from app.core.config import settings

class GeminiProvider(AIProvider):
    """Gemini AI provider"""
    
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        else:
            self.model = None
    
    async def generate_content(self, prompt: str) -> str:
        """Gemini ile içerik üret"""
        if not self.model:
            raise Exception("Gemini API key bulunamadı")
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API hatası: {str(e)}")
    
    async def check_health(self) -> Dict[str, Any]:
        """Gemini sağlık kontrolü"""
        try:
            if not settings.GEMINI_API_KEY:
                return {
                    "available": False,
                    "error": "API key eksik"
                }
            
            # Basit bir test prompt'u gönder
            test_response = self.model.generate_content("Test")
            
            return {
                "available": True,
                "model": settings.GEMINI_MODEL,
                "status": "healthy"
            }
        except Exception as e:
            return {
                "available": False,
                "error": str(e)
            }
    
    @property
    def provider_name(self) -> str:
        return "gemini"

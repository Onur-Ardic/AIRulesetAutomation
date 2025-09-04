"""
AI service factory ve manager
"""
from typing import Optional
from app.services.ai_provider import AIProvider
from app.services.gemini_provider import GeminiProvider
from app.services.openai_provider import OpenAIProvider
from app.core.config import settings

class AIService:
    """AI service manager"""
    
    def __init__(self):
        self.provider: Optional[AIProvider] = None
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Provider'ı başlat"""
        provider_name = settings.AI_PROVIDER.lower()
        
        if provider_name == "gemini":
            self.provider = GeminiProvider()
        elif provider_name == "openai":
            self.provider = OpenAIProvider()
        else:
            raise ValueError(f"Desteklenmeyen AI provider: {provider_name}")
    
    async def generate_ruleset(self, prompt: str) -> str:
        """Ruleset üret"""
        if not self.provider:
            raise Exception("AI provider başlatılamadı")
        
        return await self.provider.generate_content(prompt)
    
    async def check_health(self):
        """Sağlık kontrolü"""
        if not self.provider:
            return {
                "available": False,
                "error": "Provider başlatılamadı"
            }
        
        return await self.provider.check_health()
    
    @property
    def provider_name(self) -> str:
        """Aktif provider adı"""
        return self.provider.provider_name if self.provider else "none"

# Global AI service instance
ai_service = AIService()

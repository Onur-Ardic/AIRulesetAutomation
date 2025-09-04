"""
AI provider base class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class AIProvider(ABC):
    """AI provider için base class"""
    
    @abstractmethod
    async def generate_content(self, prompt: str) -> str:
        """İçerik üret"""
        pass
    
    @abstractmethod
    async def check_health(self) -> Dict[str, Any]:
        """Sağlık kontrolü"""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Provider adı"""
        pass

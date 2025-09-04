"""
Uygulama yapılandırma ayarları
"""
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class Settings:
    """Uygulama ayarları"""
    
    # API Ayarları
    PROJECT_NAME: str = "AI Ruleset Generator"
    PROJECT_DESCRIPTION: str = "Generate AI context rulesets from project preferences"
    VERSION: str = "1.0.0"
    
    # Server Ayarları
    HOST: str = "127.0.0.1"
    PORT: int = 8001
    DEBUG: bool = True
    
    # CORS Ayarları
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8001"
    ]
    
    # AI Provider Ayarları
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "gemini")
    
    # Gemini AI Ayarları
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # OpenAI Ayarları
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Ollama Ayarları
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    # Hugging Face Ayarları
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    HUGGINGFACE_MODEL: str = os.getenv("HUGGINGFACE_MODEL", "microsoft/DialoGPT-medium")

# Global settings instance
settings = Settings()

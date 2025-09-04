from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Backend klasörünü path'e ekle
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Backend modüllerini import et
from app.core.config import settings
from app.routers.main import router

app = FastAPI(
    title="AI Ruleset Generator",
    description="AI-powered development ruleset generator",
    version="1.0.0"
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vercel için tüm originlere izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları dahil et
app.include_router(router)

# Vercel için handler function
handler = app

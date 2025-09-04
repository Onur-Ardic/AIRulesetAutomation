from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Backend klasörünü path'e ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.app.core.config import settings
from backend.app.routers.main import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION
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
app.include_router(router, prefix="/api")

# Vercel handler
def handler(request):
    return app(request)

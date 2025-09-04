"""
Ana API endpoint'leri
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    ProjectInfo, 
    RulesetResponse, 
    HealthResponse,
    ProjectTypesResponse,
    FrameworksResponse
)
from app.services.ai_service import ai_service
from app.services.prompt_service import PromptService
import json
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=dict)
async def root():
    """Ana sayfa"""
    return {
        "message": "AI Ruleset Generator API",
        "version": "1.0.0",
        "status": "active",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Sağlık kontrolü"""
    try:
        health_data = await ai_service.check_health()
        
        return HealthResponse(
            status="healthy" if health_data.get("available", False) else "unhealthy",
            ai_provider=ai_service.provider_name,
            ai_available=health_data.get("available", False),
            message=health_data.get("error") if not health_data.get("available", False) else "All systems operational"
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            ai_provider=ai_service.provider_name,
            ai_available=False,
            message=f"Health check failed: {str(e)}"
        )

@router.post("/generate-ruleset", response_model=RulesetResponse)
async def generate_ruleset(project_info: ProjectInfo):
    """Ruleset üret"""
    try:
        # Prompt üret
        prompt = PromptService.generate_ruleset_prompt(project_info)
        
        # AI ile içerik üret
        markdown_content = await ai_service.generate_ruleset(prompt)
        
        # JSON formatında da hazırla
        json_data = {
            "project_info": project_info.dict(),
            "generated_at": datetime.now().isoformat(),
            "ai_provider": ai_service.provider_name,
            "ruleset_content": markdown_content
        }
        
        return RulesetResponse(
            markdown=markdown_content,
            json_data=json_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ruleset generation failed: {str(e)}")

@router.get("/project-types", response_model=ProjectTypesResponse)
async def get_project_types():
    """Mevcut proje türlerini getir"""
    project_types = [
        "Web Application",
        "Mobile Application", 
        "Desktop Application",
        "API/Microservice",
        "Library/Package",
        "CLI Tool",
        "E-commerce Platform",
        "Content Management System",
        "Dashboard/Admin Panel",
        "Real-time Application",
        "Machine Learning Project",
        "Blockchain Application",
        "IoT Application",
        "Game Development",
        "Other"
    ]
    
    return ProjectTypesResponse(project_types=project_types)

@router.get("/frameworks", response_model=FrameworksResponse)
async def get_frameworks():
    """Mevcut framework'leri getir"""
    frameworks = {
        "frontend": [
            "React", "Vue.js", "Angular", "Svelte", "Next.js", "Nuxt.js", 
            "Vanilla JavaScript", "jQuery", "Alpine.js", "Lit", "Other"
        ],
        "backend": [
            "Node.js/Express", "Node.js/Fastify", "Python/Django", "Python/FastAPI", 
            "Python/Flask", "Java/Spring", "C#/.NET", "PHP/Laravel", "PHP/Symfony", 
            "Ruby on Rails", "Go/Gin", "Go/Echo", "Rust/Actix", "Other"
        ],
        "mobile": [
            "React Native", "Flutter", "Swift/iOS", "Kotlin/Android", 
            "Xamarin", "Ionic", "Cordova/PhoneGap", "Other"
        ],
        "database": [
            "PostgreSQL", "MySQL", "MongoDB", "SQLite", "Redis", 
            "Cassandra", "DynamoDB", "Firebase", "Supabase", "Other"
        ]
    }
    
    return FrameworksResponse(frameworks=frameworks)

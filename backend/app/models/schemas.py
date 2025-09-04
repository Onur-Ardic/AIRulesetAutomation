"""
Pydantic model tanımları
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ProjectInfo(BaseModel):
    """Proje bilgileri modeli"""
    
    # Genel bilgiler
    project_category: str  # "frontend", "backend", "fullstack"
    project_type: str
    
    # Frontend özel alanlar
    frontend_framework: Optional[str] = None
    styling_approach: Optional[str] = None  # "css", "scss", "styled-components", "tailwind", "css-modules"
    state_management: Optional[str] = None  # "useState", "zustand", "redux-toolkit", "tanstack-query", "context"
    http_client: Optional[str] = None  # "fetch", "axios", "tanstack-query", "swr"
    ui_library: Optional[str] = None  # "none", "mui", "antd", "chakra-ui", "mantine"
    build_tool: Optional[str] = None  # "vite", "webpack", "next.js", "create-react-app"
    testing_framework: Optional[str] = None  # "jest", "vitest", "cypress", "playwright"
    
    # Backend özel alanlar
    backend_language: Optional[str] = None
    backend_framework: Optional[str] = None
    database_type: Optional[str] = None
    auth_method: Optional[str] = None  # "jwt", "session", "oauth", "passport", "auth0"
    api_style: Optional[str] = None  # "rest", "graphql", "grpc", "soap"
    orm_tool: Optional[str] = None  # "prisma", "typeorm", "sequelize", "mongoose", "sqlalchemy"
    
    # Ortak alanlar
    code_style: Optional[str] = None
    testing_requirement: bool = False
    deployment_platform: Optional[str] = None
    additional_requirements: Optional[List[str]] = []
    notes: Optional[str] = None

class RulesetResponse(BaseModel):
    """Ruleset yanıt modeli"""
    markdown: str
    json_data: Dict[str, Any]

class HealthResponse(BaseModel):
    """Sağlık kontrolü yanıt modeli"""
    status: str
    ai_provider: str
    ai_available: bool
    message: Optional[str] = None

class ProjectTypesResponse(BaseModel):
    """Proje türleri yanıt modeli"""
    project_types: List[str]

class FrameworksResponse(BaseModel):
    """Framework'ler yanıt modeli"""
    frameworks: Dict[str, List[str]]

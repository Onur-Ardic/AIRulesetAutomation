from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv
import openai
import json
import requests
from datetime import datetime
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Ruleset Generator",
    description="Generate AI context rulesets from project preferences",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ProjectInfo(BaseModel):
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
    markdown: str
    json_data: Dict[str, Any]

# AI Provider configuration
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")  # "openai", "ollama", "huggingface", "gemini"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Initialize AI clients
if AI_PROVIDER == "openai":
    openai.api_key = os.getenv("OPENAI_API_KEY")
elif AI_PROVIDER == "gemini":
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)

def generate_ruleset_prompt(project_info: ProjectInfo) -> str:
    """Generate a detailed prompt for the AI to create a ruleset based on project category"""
    
    # Temel bilgiler
    base_info = f"""
Create a comprehensive project ruleset for an AI coding assistant (like Copilot, Cursor, or ChatGPT). 
This ruleset should serve as context for generating high-quality, consistent code.

PROJECT CATEGORY: {project_info.project_category.upper()}
PROJECT TYPE: {project_info.project_type}
"""

    # Kategori-özel bilgiler
    if project_info.project_category == "frontend":
        tech_details = f"""
FRONTEND TECHNOLOGY STACK:
- Framework: {project_info.frontend_framework or 'Not specified'}
- Styling Approach: {project_info.styling_approach or 'Standard CSS'}
- State Management: {project_info.state_management or 'Component state'}
- HTTP Client: {project_info.http_client or 'Fetch API'}
- UI Library: {project_info.ui_library or 'None'}
- Build Tool: {project_info.build_tool or 'Standard bundler'}
- Testing Framework: {project_info.testing_framework or 'Not specified'}
"""
        
        specific_sections = """
Generate a detailed markdown ruleset that includes:

1. **Agent Role Definition** - Frontend developer persona for AI assistants
2. **Technology Stack** - Specific frontend technologies and their usage patterns
3. **Component Architecture** - Component structure, atomic design, file organization
4. **Styling Guidelines** - CSS/SCSS/Styled-components best practices
5. **State Management** - How to handle local and global state
6. **API Integration** - HTTP client usage, data fetching patterns
7. **Performance Optimization** - Bundle size, lazy loading, memoization
8. **Accessibility Standards** - A11Y guidelines and semantic HTML
9. **Testing Strategy** - Unit, integration, and E2E testing approaches
10. **Code Organization** - File structure, naming conventions
11. **Development Workflow** - Git workflow, PR guidelines, code review
12. **Build and Deployment** - Bundling, optimization, deployment strategies
"""

    elif project_info.project_category == "backend":
        tech_details = f"""
BACKEND TECHNOLOGY STACK:
- Language: {project_info.backend_language or 'Not specified'}
- Framework: {project_info.backend_framework or 'Not specified'}
- Database: {project_info.database_type or 'Not specified'}
- Authentication: {project_info.auth_method or 'Basic auth'}
- API Style: {project_info.api_style or 'REST'}
- ORM/Database Tool: {project_info.orm_tool or 'Native queries'}
"""
        
        specific_sections = """
Generate a detailed markdown ruleset that includes:

1. **Agent Role Definition** - Backend developer persona for AI assistants
2. **Technology Stack** - Specific backend technologies and frameworks
3. **API Design Principles** - RESTful/GraphQL design patterns
4. **Database Design** - Schema design, migrations, queries
5. **Authentication & Authorization** - Security patterns and implementations
6. **Error Handling** - Exception management and error responses
7. **Testing Strategy** - Unit, integration, and API testing
8. **Performance & Optimization** - Caching, indexing, query optimization
9. **Security Guidelines** - Input validation, SQL injection prevention
10. **Code Architecture** - Clean architecture, SOLID principles
11. **Documentation Standards** - API documentation, code comments
12. **Deployment & DevOps** - Containerization, CI/CD, monitoring
"""

    else:  # fullstack
        tech_details = f"""
FULLSTACK TECHNOLOGY STACK:
Frontend:
- Framework: {project_info.frontend_framework or 'Not specified'}
- Styling: {project_info.styling_approach or 'Standard CSS'}
- State Management: {project_info.state_management or 'Component state'}
- HTTP Client: {project_info.http_client or 'Fetch API'}

Backend:
- Language: {project_info.backend_language or 'Not specified'}
- Framework: {project_info.backend_framework or 'Not specified'}
- Database: {project_info.database_type or 'Not specified'}
- API Style: {project_info.api_style or 'REST'}
"""
        
        specific_sections = """
Generate a detailed markdown ruleset that includes:

1. **Agent Role Definition** - Fullstack developer persona for AI assistants
2. **Technology Stack** - Complete frontend and backend technologies
3. **Project Architecture** - Monorepo vs separate repos, folder structure
4. **Frontend Guidelines** - Component architecture, styling, state management
5. **Backend Guidelines** - API design, database patterns, authentication
6. **API Integration** - Frontend-backend communication patterns
7. **Shared Standards** - TypeScript types, validation schemas, error handling
8. **Testing Strategy** - Comprehensive testing across the stack
9. **Development Workflow** - Full-stack development patterns
10. **Performance Optimization** - End-to-end performance considerations
11. **Security & Authentication** - Full-stack security implementation
12. **Deployment Strategy** - Coordinated frontend-backend deployment
"""

    # Ortak bilgiler
    common_details = f"""
ADDITIONAL DETAILS:
- Code Style: {project_info.code_style or 'Standard'}
- Testing Required: {'Yes' if project_info.testing_requirement else 'No'}
- Deployment Platform: {project_info.deployment_platform or 'Not specified'}
- Additional Requirements: {', '.join(project_info.additional_requirements) if project_info.additional_requirements else 'None'}
- Notes: {project_info.notes or 'None'}
"""

    # Template stil bilgisi (MD dosyasından esinlenerek)
    style_guide = """
The ruleset should be:
- Written in Turkish and English (bilingual sections)
- Specific to the chosen technologies
- Actionable and clear with code examples
- Suitable for AI assistant context
- Professional and comprehensive
- Include practical examples and code snippets
- Provide PR templates and checklists
- Reference modern best practices

Format the response as proper Markdown with clear headers, bullet points, and code examples.
Include sections in both Turkish and English for international teams.
"""

    return f"""
Sen bir uzman yazılım geliştirici ve AI asistan rehberi uzmanısın. 

Aşağıdaki proje bilgilerine göre, GitHub Copilot, Cursor AI, ChatGPT gibi AI kodlama asistanları için kapsamlı bir TÜRKÇE ruleset/rehber oluştur.

PROJE BİLGİLERİ:
- Kategori: {project_info.project_category.upper()}
- Proje Türü: {project_info.project_type}
- Kod Stili: {project_info.code_style or 'Standart'}
- Test Gereksinimi: {'Evet' if project_info.testing_requirement else 'Hayır'}
- Deployment: {project_info.deployment_platform or 'Belirtilmemiş'}

{tech_details}

EK GEREKSINIMLER:
{', '.join(project_info.additional_requirements) if project_info.additional_requirements else 'Yok'}

NOTLAR:
{project_info.notes or 'Yok'}

OLUŞTURACAĞIN RULESET ŞU YAPIDA OLMALI:

# 🤖 AI Geliştirici Asistan Rehberi
## {project_info.project_category.title()} Projesi İçin Kapsamlı Kural Seti

### 📋 Proje Özeti
[Proje bilgilerini özetle]

### 🎯 AI Asistan Rolü ve Sorumlulukları

Sen bu projede uzman bir {project_info.project_category} geliştiricisisin. Görevlerin:

- ✅ Belirtilen teknoloji stack'ini kullanarak kod üretmek
- ✅ Best practices ve modern yaklaşımları uygulamak
- ✅ Temiz, okunabilir ve maintainable kod yazmak
- ✅ Performans optimizasyonlarını göz önünde bulundurmak
- ✅ Security standartlarına uygun kod üretmek

### 🛠️ Teknoloji Stack Detayları

[Kullanılan teknolojilerin detaylı açıklaması]

### 📁 Proje Yapısı ve Organizasyon

```
[Önerilen klasör yapısı]
```

### 🎨 Kod Yazım Standartları

#### Genel Kurallar:
- Kod yazarken Türkçe yorum satırları kullan
- Değişken ve fonksiyon isimleri İngilizce olsun
- Clean Code prensiplerini uygula

#### Örnek Kod Yapısı:
```javascript
// Doğru kullanım örneği
```

### 🔧 Geliştirme Workflow'u

#### Git Workflow:
- Feature branch kullanımı
- Commit message standartları
- PR template'i

#### Kod Review Checklist:
- [ ] Kod standartlara uygun mu?
- [ ] Test coverage yeterli mi?
- [ ] Performance etkileri değerlendirildi mi?

### 🧪 Test Stratejisi

[Test yaklaşımları ve örnekler]

### 🚀 Performance ve Optimizasyon

[Performance best practices]

### 🔒 Güvenlik Kuralları

[Security guidelines]

### 📚 Referanslar ve Kaynaklar

[Faydalı linkler ve dökümanlar]

### 🎯 Özel Durumlar ve İpuçları

[Proje-spesifik öneriler]

### 📝 Pull Request Template

```markdown
## PR Açıklaması
- [ ] Yapılan değişiklikler açıklandı
- [ ] Test senaryoları eklendi
- [ ] Dokümantasyon güncellendi
```

### 🚦 Definition of Done

- [ ] Kod review tamamlandı
- [ ] Testler yazıldı ve geçiyor
- [ ] Dokümantasyon güncellendi
- [ ] Performance etkileri değerlendirildi

ÖNEMLI: 
- Türkçe ve anlaşılır bir dil kullan
- Praktik örnekler ve kod snippet'leri ekle
- Projenin özel gereksinimlerini dikkate al
- Modern best practices'i referans al
- AI asistanların anlayabileceği net ve spesifik talimatlar ver
"""

async def call_ai_api(prompt: str) -> str:
    """Call AI API based on configured provider"""
    
    if AI_PROVIDER == "openai":
        return await call_openai_api(prompt)
    elif AI_PROVIDER == "ollama":
        return await call_ollama_api(prompt)
    elif AI_PROVIDER == "huggingface":
        return await call_huggingface_api(prompt)
    elif AI_PROVIDER == "gemini":
        return await call_gemini_api(prompt)
    else:
        raise HTTPException(status_code=500, detail=f"Unsupported AI provider: {AI_PROVIDER}")

async def call_openai_api(prompt: str) -> str:
    """Call OpenAI API to generate ruleset"""
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert software architect and technical writer specializing in creating comprehensive development guidelines and rulesets for AI coding assistants."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

async def call_ollama_api(prompt: str) -> str:
    """Call Ollama API (local AI) to generate ruleset"""
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": "You are an expert software architect and technical writer specializing in creating comprehensive development guidelines and rulesets for AI coding assistants. Provide detailed, actionable guidelines in markdown format."},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("message", {}).get("content", "")
        else:
            raise HTTPException(status_code=500, detail=f"Ollama API error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=500, 
            detail="Ollama sunucusuna bağlanılamıyor. Ollama'nın kurulu ve çalışır durumda olduğundan emin olun. Kurulum: https://ollama.ai"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama API error: {str(e)}")

async def call_huggingface_api(prompt: str) -> str:
    """Call Hugging Face API to generate ruleset"""
    try:
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Using a free model like Microsoft DialoGPT
        payload = {
            "inputs": f"System: You are an expert software architect. Create a comprehensive development ruleset in markdown format.\n\nUser: {prompt}",
            "parameters": {
                "max_new_tokens": 1500,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
            return str(result)
        else:
            raise HTTPException(status_code=500, detail=f"Hugging Face API error: {response.text}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hugging Face API error: {str(e)}")

async def call_gemini_api(prompt: str) -> str:
    """Call Google Gemini API to generate ruleset"""
    try:
        if not GEMINI_API_KEY:
            raise HTTPException(
                status_code=500, 
                detail="Gemini API key bulunamadı. GEMINI_API_KEY environment variable'ını ayarlayın."
            )
        
        # Initialize Gemini model
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        # System instruction for better responses
        system_instruction = """Sen uzman bir yazılım mimarı ve teknik yazar olarak, AI kodlama asistanları için kapsamlı geliştirme rehberleri oluşturma konusunda uzmanlaşmışsın. 

Görevin:
- Detaylı, uygulanabilir ve açık rehberler yazmak
- Türkçe dilinde profesyonel içerik üretmek
- Modern best practice'leri kullanmak
- AI asistanların anlayabileceği net talimatlar vermek
- Kod örnekleri ve pratik uygulamalar eklemek

Lütfen markdown formatında, düzenli başlıklar ve madde işaretleri ile yapılandırılmış bir rehber oluştur."""

        # Prepare the full prompt
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        # Generate content
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                top_k=40,
                max_output_tokens=4000,
            )
        )
        
        if response.text:
            return response.text
        else:
            raise HTTPException(
                status_code=500,
                detail="Gemini API'den boş yanıt alındı"
            )
            
    except Exception as e:
        # Handle specific Gemini errors
        if "API_KEY_INVALID" in str(e):
            raise HTTPException(
                status_code=401,
                detail="Geçersiz Gemini API key. Lütfen doğru API key'i kontrol edin."
            )
        elif "QUOTA_EXCEEDED" in str(e):
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota'sı aşıldı. Lütfen daha sonra tekrar deneyin."
            )
        elif "SAFETY" in str(e):
            raise HTTPException(
                status_code=400,
                detail="İçerik güvenlik filtresi tarafından engellendi. Lütfen daha uygun bir prompt deneyin."
            )
        else:
            raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

def markdown_to_json(markdown_content: str, project_info: ProjectInfo) -> Dict[str, Any]:
    """Convert markdown ruleset to structured JSON"""
    
    json_data = {
        "project_category": project_info.project_category,
        "project_type": project_info.project_type,
        
        # Frontend özel alanlar
        "frontend_framework": project_info.frontend_framework,
        "styling_approach": project_info.styling_approach,
        "state_management": project_info.state_management,
        "http_client": project_info.http_client,
        "ui_library": project_info.ui_library,
        "build_tool": project_info.build_tool,
        "testing_framework": project_info.testing_framework,
        
        # Backend özel alanlar
        "backend_language": project_info.backend_language,
        "backend_framework": project_info.backend_framework,
        "database_type": project_info.database_type,
        "auth_method": project_info.auth_method,
        "api_style": project_info.api_style,
        "orm_tool": project_info.orm_tool,
        
        # Ortak alanlar
        "code_style": project_info.code_style,
        "testing_requirement": project_info.testing_requirement,
        "deployment_platform": project_info.deployment_platform,
        "additional_requirements": project_info.additional_requirements,
        "notes": project_info.notes,
        
        "generated_ruleset": markdown_content,
        "timestamp": datetime.now().isoformat()
    }
    
    return json_data

@app.get("/")
async def root():
    return {"message": "AI Ruleset Generator API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    ai_status = "unknown"
    additional_info = {}
    
    if AI_PROVIDER == "ollama":
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            ai_status = "connected" if response.status_code == 200 else "disconnected"
            additional_info = {
                "ollama_url": OLLAMA_BASE_URL,
                "ollama_model": OLLAMA_MODEL
            }
        except:
            ai_status = "disconnected"
            additional_info = {
                "ollama_url": OLLAMA_BASE_URL,
                "ollama_model": OLLAMA_MODEL
            }
    elif AI_PROVIDER == "openai":
        ai_status = "configured" if os.getenv("OPENAI_API_KEY") else "not_configured"
    elif AI_PROVIDER == "huggingface":
        ai_status = "configured" if os.getenv("HUGGINGFACE_API_KEY") else "not_configured"
    elif AI_PROVIDER == "gemini":
        ai_status = "configured" if GEMINI_API_KEY else "not_configured"
        additional_info = {
            "gemini_model": GEMINI_MODEL
        }
        
        # Test Gemini API connection if configured
        if ai_status == "configured":
            try:
                # Simple test to check if API key works
                model = genai.GenerativeModel('gemini-pro')
                test_response = model.generate_content("Test", 
                    generation_config=genai.types.GenerationConfig(max_output_tokens=10))
                ai_status = "connected" if test_response else "api_error"
            except Exception as e:
                if "API_KEY_INVALID" in str(e):
                    ai_status = "invalid_api_key"
                else:
                    ai_status = "connection_error"
    
    return {
        "status": "healthy",
        "ai_provider": AI_PROVIDER,
        "ai_status": ai_status,
        **additional_info
    }

@app.post("/generate-ruleset", response_model=RulesetResponse)
async def generate_ruleset(project_info: ProjectInfo):
    """Generate a project ruleset based on user input"""
    
    try:
        # Generate prompt
        prompt = generate_ruleset_prompt(project_info)
          # Call AI API
        markdown_content = await call_ai_api(prompt)
        
        # Convert to JSON structure
        json_data = markdown_to_json(markdown_content, project_info)
        
        return RulesetResponse(
            markdown=markdown_content,
            json_data=json_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ruleset: {str(e)}")

@app.get("/project-categories")
async def get_project_categories():
    """Get available project categories and their specific options"""
    return {
        "categories": [
            "frontend",
            "backend", 
            "fullstack"
        ],
        "frontend_options": {
            "frameworks": ["React", "Vue.js", "Angular", "Svelte", "Next.js", "Nuxt.js", "Vanilla JS"],
            "styling_approaches": ["CSS", "SCSS/SASS", "Styled Components", "Tailwind CSS", "CSS Modules", "Emotion"],
            "state_management": ["useState/useReducer", "Zustand", "Redux Toolkit", "TanStack Query", "Context API", "Valtio"],
            "http_clients": ["Fetch API", "Axios", "TanStack Query", "SWR", "Apollo Client"],
            "ui_libraries": ["None", "Material-UI", "Ant Design", "Chakra UI", "Mantine", "React Bootstrap"],
            "build_tools": ["Vite", "Webpack", "Next.js", "Create React App", "Parcel"],
            "testing_frameworks": ["Jest", "Vitest", "Cypress", "Playwright", "React Testing Library"]
        },
        "backend_options": {
            "languages": ["Python", "JavaScript/Node.js", "Java", "C#", "Go", "Rust", "PHP", "Ruby"],
            "frameworks": ["FastAPI", "Django", "Flask", "Express.js", "Spring Boot", "ASP.NET Core", "Gin", "Laravel"],
            "databases": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Firebase", "Supabase"],
            "auth_methods": ["JWT", "Session-based", "OAuth 2.0", "Passport.js", "Auth0", "Firebase Auth"],
            "api_styles": ["REST", "GraphQL", "gRPC", "SOAP", "WebSocket"],
            "orm_tools": ["Prisma", "TypeORM", "Sequelize", "Mongoose", "SQLAlchemy", "Hibernate"]
        },
        "common_options": {
            "project_types": ["Web Application", "Mobile App", "Desktop Application", "API/Microservice", "CLI Tool", "Library/Package"],
            "deployment_platforms": ["AWS", "Google Cloud", "Azure", "Vercel", "Netlify", "Heroku", "Docker", "Railway"],
            "code_styles": ["Standard", "Prettier", "ESLint", "Airbnb", "Google", "PEP8"]
        }
    }

@app.get("/frameworks")
async def get_frameworks():
    """Get available frameworks by category"""
    return {
        "backend_languages": ["Python", "JavaScript/Node.js", "Java", "C#", "Go", "Rust", "PHP", "Ruby"],
        "backend_frameworks": ["FastAPI", "Django", "Flask", "Express.js", "Spring Boot", "ASP.NET Core", "Gin", "Laravel"],
        "frontend_frameworks": ["React", "Vue.js", "Angular", "Svelte", "Next.js", "Nuxt.js", "Vanilla JS"],
        "databases": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Firebase", "Supabase"],
        "deployment_platforms": ["AWS", "Google Cloud", "Azure", "Vercel", "Netlify", "Heroku", "Docker", "Railway"]
    }

@app.post("/test-gemini")
async def test_gemini_connection():
    """Test Gemini AI API connection and model response"""
    if AI_PROVIDER != "gemini":
        raise HTTPException(
            status_code=400,
            detail="AI provider 'gemini' olarak ayarlanmalı. Şu anki provider: " + AI_PROVIDER
        )
    
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=400,
            detail="GEMINI_API_KEY environment variable ayarlanmalı"
        )
    
    try:
        test_prompt = "Python FastAPI için basit bir Hello World örneği oluştur."
        result = await call_gemini_api(test_prompt)
        
        return {
            "status": "success",
            "model_used": GEMINI_MODEL,
            "test_prompt": test_prompt,
            "response_preview": result[:200] + "..." if len(result) > 200 else result,
            "full_response_length": len(result)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini test başarısız: {str(e)}"
        )

@app.get("/gemini-models")
async def get_gemini_models():
    """Get available Gemini models and their configurations"""
    return {
        "current_model": GEMINI_MODEL,
        "available_models": {
            "gemini-1.5-flash": {
                "name": "Gemini 1.5 Flash",
                "description": "Hızlı ve verimli, günlük kullanım için ideal",
                "best_for": "Hızlı yanıtlar, basit görevler",
                "max_tokens": 8192,
                "cost": "Düşük"
            },
            "gemini-1.5-pro": {
                "name": "Gemini 1.5 Pro", 
                "description": "Yüksek kaliteli, karmaşık görevler için",
                "best_for": "Kod generation, teknik rehberler, analiz",
                "max_tokens": 32768,
                "cost": "Orta"
            },
            "gemini-pro": {
                "name": "Gemini Pro",
                "description": "Dengeli performans ve kalite",
                "best_for": "Genel amaçlı kullanım",
                "max_tokens": 4096,
                "cost": "Orta"
            }
        },
        "setup_instructions": {
            "step1": "https://makersuite.google.com/app/apikey adresinden API key alın",
            "step2": "GEMINI_API_KEY environment variable'ını ayarlayın",
            "step3": "GEMINI_MODEL ile model seçin (opsiyonel)",
            "step4": "AI_PROVIDER=gemini olarak ayarlayın"
        },
        "rate_limits": {
            "free_tier": "15 request/minute",
            "paid_tier": "1000 request/minute",
            "note": "Ücretsiz tier günlük limit var"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

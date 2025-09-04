"""
Ruleset prompt generation service
"""
from app.models.schemas import ProjectInfo

class PromptService:
    """Prompt üretimi için service"""
    
    @staticmethod
    def generate_ruleset_prompt(project_info: ProjectInfo) -> str:
        """Proje bilgilerine göre ruleset prompt'u üret"""
        
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
- Frontend Framework: {project_info.frontend_framework or 'Not specified'}
- Backend Language: {project_info.backend_language or 'Not specified'}
- Backend Framework: {project_info.backend_framework or 'Not specified'}
- Database: {project_info.database_type or 'Not specified'}
- Authentication: {project_info.auth_method or 'Basic auth'}
"""
            
            specific_sections = """
Generate a detailed markdown ruleset that includes:

1. **Agent Role Definition** - Full-stack developer persona for AI assistants
2. **Technology Stack** - Complete frontend and backend technologies
3. **Project Architecture** - Monorepo vs separate repos, folder structure
4. **API Design** - Backend API design and frontend integration
5. **Database Design** - Schema design and frontend data handling
6. **Authentication Flow** - End-to-end auth implementation
7. **State Management** - Frontend state with backend synchronization
8. **Testing Strategy** - Full-stack testing approach
9. **Performance** - Both frontend and backend optimization
10. **Security** - Comprehensive security measures
11. **Development Workflow** - Full-stack development practices
12. **Deployment** - Complete application deployment strategy
"""

        # Ortak gereksinimler
        common_requirements = f"""
ADDITIONAL REQUIREMENTS:
- Code Style: {project_info.code_style or 'Standard conventions'}
- Testing Required: {'Yes' if project_info.testing_requirement else 'No'}
- Deployment Platform: {project_info.deployment_platform or 'Not specified'}
- Additional Requirements: {', '.join(project_info.additional_requirements) if project_info.additional_requirements else 'None'}
- Notes: {project_info.notes or 'None'}
"""

        # Çıktı formatı
        output_format = """
IMPORTANT FORMATTING REQUIREMENTS:
1. Use proper markdown formatting with headers, lists, and code blocks
2. Include specific code examples where relevant
3. Make rules actionable and specific, not generic
4. Include file structure examples
5. Provide concrete examples of good vs bad practices
6. Include relevant package/dependency recommendations
7. Make the ruleset ready to copy-paste as context for AI assistants

Format the output as a comprehensive markdown document that can be directly used as context for AI coding assistants.
"""

        return base_info + tech_details + specific_sections + common_requirements + output_format

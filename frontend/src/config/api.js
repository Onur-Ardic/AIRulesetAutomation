// API Base URL Configuration
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://ai-ruleset-generator-2024.vercel.app'  // Vercel backend URL'ni buraya koy
  : 'http://localhost:8001';  // Local development

export default API_BASE_URL;

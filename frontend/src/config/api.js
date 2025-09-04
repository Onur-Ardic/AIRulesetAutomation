// API Base URL Configuration
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api'  // Vercel production'da /api prefix kullanır
  : 'http://localhost:8001';  // Local development

export default API_BASE_URL;

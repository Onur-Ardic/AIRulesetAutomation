# 🤖 AI Ruleset Generator

Proje tercihlerinizi yapay zeka asistanları (Copilot, Cursor, ChatGPT) için optimize edilmiş kurallar setine dönüştüren web uygulaması.

## 🚀 Özellikler

- **Akıllı Form**: Proje türü, teknoloji stack'i ve tercihlerinizi kolayca girin
- **Çoklu AI Desteği**: Ollama (ücretsiz, yerel), OpenAI (ücretli), Hugging Face (ücretsiz API)
- **Çoklu Format**: Markdown ve JSON formatlarında çıktı
- **Instant Download**: Ruleset'leri doğrudan indirin
- **Modern UI**: Responsive ve kullanıcı dostu arayüz
- **AI Context Ready**: Popüler AI araçlarıyla uyumlu format

## 🆓 AI Provider Seçenekleri

### 1. 🔥 Ollama (ÖNERİLEN - ÜCRETSİZ)
- **Avantajlar**: Tamamen ücretsiz, yerel çalışır, gizlilik
- **Kurulum**: https://ollama.ai
- **Modeller**: llama3.2, mistral, codellama ve daha fazlası

### 2. 💰 OpenAI
- **Avantajlar**: Yüksek kalite, hızlı
- **Dezavantajlar**: Ücretli ($0.002/1K token)
- **API Key**: https://platform.openai.com/api-keys

### 3. 🌐 Hugging Face
- **Avantajlar**: Ücretsiz API
- **Dezavantajlar**: Rate limiting, daha düşük kalite
- **Token**: https://huggingface.co/settings/tokens

## 🛠️ Teknoloji Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Çoklu AI Desteği** - Ollama, OpenAI, Hugging Face
- **Uvicorn** - ASGI server
- **Pydantic** - Veri validasyonu

### Frontend
- **React 18** - Modern UI framework
- **Axios** - HTTP client
- **React Markdown** - Markdown rendering
- **Modern CSS** - Glassmorphism design

## 📦 Kurulum

### ⚡ Hızlı Başlangıç (Önerilen)

```powershell
# 1. Projeyi klonlayın
git clone <repository-url>
cd AIRuleset

# 2. Otomatik kurulum
npm run setup

# 3. Tüm servisleri başlat
npm start
```

**VE HEPSİ BU! 🎉**

### 🎮 Kullanılabilir Komutlar

```powershell
npm start           # 🚀 Tüm servisleri başlat
npm stop            # 🛑 Tüm servisleri durdur  
npm run status      # 📊 Durum kontrolü
npm run setup       # 🛠️  İlk kurulum
```

**Windows Kullanıcıları için:**
- `start.bat` - Çift tıklayarak başlat
- `stop.bat` - Çift tıklayarak durdur

### 📋 Manuel Kurulum

#### 1. Gereksinimler
- **Python 3.8+**
- **Node.js 16+**
- **Ollama** (https://ollama.ai) - ÜCRETSİZ

#### 2. Backend Kurulumu

```powershell
# Backend klasörüne git
cd backend

# Virtual environment oluştur (opsiyonel ama önerilir)
python -m venv venv
.\venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Environment variables ayarla
copy .env.example .env
# .env dosyasını düzenleyip AI provider'ınızı seçin
```

#### 3. AI Provider Kurulumu

##### Seçenek A: Ollama (ÜCRETSİZ - ÖNERİLEN)
```powershell
# 1. Ollama'yı indirin ve kurun: https://ollama.ai
# 2. Model indirin
ollama pull llama3.2

# 3. .env dosyasında:
AI_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

#### Seçenek B: OpenAI (ÜCRETLİ)
```powershell
# .env dosyasında:
AI_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
```

#### Seçenek C: Hugging Face (ÜCRETSİZ API)
```powershell
# .env dosyasında:
AI_PROVIDER=huggingface
HUGGINGFACE_API_KEY=your_token_here
```

### 4. Frontend Kurulumu

```powershell
# Frontend klasörüne git
cd frontend

# Node modules yükle
npm install
```

## 🏃‍♂️ Çalıştırma

### Terminal 1 - Backend
```powershell
cd backend
# Virtual environment aktif ise
.\venv\Scripts\activate
# Sunucuyu başlat
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```
Backend: http://localhost:8000

### Terminal 2 - Frontend  
```powershell
cd frontend
npm start
```
Frontend: http://localhost:3000

## 📚 Kullanım

1. **Web uygulamasını açın**: http://localhost:3000
2. **Proje bilgilerini girin**:
   - Proje türü (Web App, Mobile App, vb.)
   - Backend dili ve framework
   - Frontend framework
   - Veritabanı tercihi
   - Kod stili tercihleri
   - Test gereksinimleri
   - Ek notlar

3. **Ruleset oluşturun**: "🚀 Ruleset Oluştur" butonuna tıklayın
4. **Sonuçları görüntüleyin**: Markdown veya JSON formatında
5. **İndirin**: `.md` veya `.json` dosyası olarak

## 🎯 AI Araçlarıyla Kullanım

### GitHub Copilot
```bash
# Proje kök dizininize kaydedin
.copilot-rules.md
```

### Cursor IDE
```bash
# Proje kök dizininize kaydedin  
.cursorrules
```

### ChatGPT/Claude
Kod geliştirme isteklerinizin başında context olarak kullanın:

```
Bu ruleset'e göre kod geliştir: [ruleset içeriği]
```

## 🔧 API Endpoints

### Backend API
- `GET /` - API status
- `GET /health` - Health check
- `POST /generate-ruleset` - Ruleset üretimi
- `GET /project-types` - Mevcut proje türleri
- `GET /frameworks` - Mevcut framework'ler

### API Dokumentasyonu
Swagger UI: http://localhost:8000/docs

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🆘 Sorun Giderme

### Backend Sorunları
- **OpenAI API hatası**: `.env` dosyasında API key'inizi kontrol edin
- **Port çakışması**: `main.py`'da farklı port kullanın
- **CORS hatası**: CORS ayarlarını `main.py`'da kontrol edin

### Frontend Sorunları  
- **API bağlantısı**: Backend'in çalıştığından emin olun
- **Port çakışması**: `package.json`'da farklı port belirleyin

## 🔮 Gelecek Özellikler

- [ ] Ollama desteği (yerel AI)
- [ ] Anthropic Claude entegrasyonu
- [ ] Özel template desteği
- [ ] Ruleset versiyonlama
- [ ] Team collaboration
- [ ] Template marketplace

---

**AI Ruleset Generator v1.0** - Yapay Zeka Destekli Geliştirme Için 🚀

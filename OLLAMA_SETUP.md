# 🦙 Ollama Kurulum Rehberi (ÜCRETSİZ AI)

Ollama, yerel bilgisayarınızda AI modelleri çalıştırmanıza olanak sağlayan ücretsiz bir araçtır.

## 📥 Kurulum Adımları

### 1. Ollama'yı İndirin
- **Windows**: https://ollama.ai/download/windows
- **macOS**: https://ollama.ai/download/mac  
- **Linux**: https://ollama.ai/download/linux

### 2. Kurulum
```powershell
# Windows için .exe dosyasını çalıştırın
# İndirilen dosyayı çift tıklayın ve kurulum sihirbazını takip edin
```

### 3. Model İndirin
```powershell
# Terminal/CMD açın ve şu komutları çalıştırın:

# Küçük ve hızlı model (önerilen)
ollama pull llama3.2

# Alternatif modeller:
# ollama pull mistral        # Daha kompakt
# ollama pull codellama      # Kod odaklı
# ollama pull llama3.2:3b    # Çok küçük ve hızlı
```

### 4. Test Edin
```powershell
# Ollama'nın çalıştığını test edin
ollama list

# Model ile sohbet test edin
ollama run llama3.2
```

### 5. AI Ruleset Generator'da Ayarlayın
```env
# backend/.env dosyasında:
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

## 📊 Model Karşılaştırması

| Model | Boyut | Hız | Kalite | RAM Gereksinimi |
|-------|-------|-----|--------|-----------------|
| llama3.2:3b | 2GB | ⚡⚡⚡ | ⭐⭐⭐ | 4GB |
| llama3.2 | 4.7GB | ⚡⚡ | ⭐⭐⭐⭐ | 8GB |
| mistral | 4.1GB | ⚡⚡ | ⭐⭐⭐⭐ | 8GB |
| codellama | 3.8GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | 8GB (kod için) |

## ⚡ Performans İpuçları

1. **RAM**: En az 8GB RAM önerilir
2. **SSD**: Model dosyaları için SSD kullanın
3. **GPU**: NVIDIA GPU varsa otomatik olarak kullanılır
4. **Model Seçimi**: İlk defa kullanıyorsanız `llama3.2:3b` ile başlayın

## 🔧 Sorun Giderme

### Ollama Başlamıyor
```powershell
# Servisi manuel başlatın
ollama serve
```

### Port Sorunu
```env
# .env dosyasında farklı port kullanın
OLLAMA_BASE_URL=http://localhost:11435
```

### Model İndirilmiyor
```powershell
# İnternet bağlantınızı kontrol edin
# Proxy kullanıyorsanız ayarları yapın
ollama pull llama3.2:3b  # Daha küçük model deneyin
```

## 🌟 Avantajları

- ✅ **Tamamen Ücretsiz**: Hiçbir API ücreti yok
- ✅ **Gizlilik**: Verileriniz yerel kalır
- ✅ **Offline**: İnternet bağlantısı gerektirmez
- ✅ **Hızlı**: Yerel işlem
- ✅ **Çok Sayıda Model**: 50+ model seçeneği

## 📚 Ek Kaynaklar

- **Resmi Dokümantasyon**: https://ollama.ai/docs
- **Model Kütüphanesi**: https://ollama.ai/library
- **GitHub**: https://github.com/ollama/ollama
- **Discord Topluluğu**: https://discord.gg/ollama

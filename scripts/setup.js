#!/usr/bin/env node

const { spawn } = require('cross-spawn');
const path = require('path');
const fs = require('fs');

// Renkli console output için
const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

async function setupProject() {
    log('🛠️  AI Ruleset Generator İlk Kurulum\n', 'blue');
    
    try {
        // 1. Ana dizin node modules
        log('📦 Ana dizin bağımlılıkları yükleniyor...', 'blue');
        const mainInstall = spawn.sync('npm', ['install'], { 
            cwd: __dirname,
            stdio: 'inherit' 
        });
        if (mainInstall.status === 0) {
            log('✅ Ana dizin bağımlılıkları yüklendi', 'green');
        } else {
            throw new Error('Ana dizin npm install başarısız');
        }
        
        // 2. Frontend bağımlılıkları
        log('🎨 Frontend bağımlılıkları yükleniyor...', 'cyan');
        const frontendPath = path.join(__dirname, '..', 'frontend');
        const frontendInstall = spawn.sync('npm', ['install'], { 
            cwd: frontendPath,
            stdio: 'inherit' 
        });
        if (frontendInstall.status === 0) {
            log('✅ Frontend bağımlılıkları yüklendi', 'green');
        } else {
            throw new Error('Frontend npm install başarısız');
        }
        
        // 3. Backend bağımlılıkları
        log('⚙️  Backend bağımlılıkları yükleniyor...', 'blue');
        const backendPath = path.join(__dirname, '..', 'backend');
        const backendInstall = spawn.sync('pip', ['install', '-r', 'requirements.txt'], { 
            cwd: backendPath,
            stdio: 'inherit' 
        });
        if (backendInstall.status === 0) {
            log('✅ Backend bağımlılıkları yüklendi', 'green');
        } else {
            throw new Error('Backend pip install başarısız');
        }
        
        // 4. .env dosyası kontrolü
        log('📝 Konfigürasyon dosyaları kontrol ediliyor...', 'yellow');
        const envPath = path.join(backendPath, '.env');
        if (!fs.existsSync(envPath)) {
            const envContent = `# AI Provider Seçimi
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Diğer ayarlar
DEBUG=True
ENVIRONMENT=development
`;
            fs.writeFileSync(envPath, envContent);
            log('✅ .env dosyası oluşturuldu', 'green');
        } else {
            log('✅ .env dosyası mevcut', 'green');
        }
        
        // 5. Ollama kontrol
        log('🦙 Ollama kontrolü yapılıyor...', 'magenta');
        try {
            const ollama = spawn.sync('ollama', ['--version'], { encoding: 'utf8' });
            if (ollama.status === 0) {
                log('✅ Ollama kurulu', 'green');
                
                // Model kontrolü
                const models = spawn.sync('ollama', ['list'], { encoding: 'utf8' });
                if (models.status === 0 && models.stdout.includes('llama3.2')) {
                    log('✅ llama3.2 modeli mevcut', 'green');
                } else {
                    log('📥 llama3.2 modeli indiriliyor...', 'yellow');
                    const pullModel = spawn.sync('ollama', ['pull', 'llama3.2'], { 
                        stdio: 'inherit' 
                    });
                    if (pullModel.status === 0) {
                        log('✅ llama3.2 modeli indirildi', 'green');
                    } else {
                        log('⚠️  Model indirme başarısız, manuel olarak çalıştırın: ollama pull llama3.2', 'yellow');
                    }
                }
            } else {
                throw new Error('Ollama bulunamadı');
            }
        } catch (e) {
            log('❌ Ollama bulunamadı!', 'red');
            log('📥 Lütfen https://ollama.ai adresinden Ollama\'yı indirin ve kurun.', 'yellow');
            log('📝 Kurulum sonrası: ollama pull llama3.2', 'yellow');
        }
        
        console.log();
        log('🎉 Kurulum tamamlandı!', 'green');
        log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'green');
        log('🚀 Başlatmak için: npm start', 'cyan');
        log('📊 Durum kontrol: npm run status', 'cyan');
        log('🛑 Durdurmak için: npm stop', 'cyan');
        
    } catch (error) {
        log(`❌ Kurulum hatası: ${error.message}`, 'red');
        process.exit(1);
    }
}

setupProject();

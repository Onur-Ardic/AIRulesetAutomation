#!/usr/bin/env node

const { spawn } = require('cross-spawn');
const path = require('path');
const fs = require('fs');

console.log('🚀 AI Ruleset Generator Başlatılıyor...\n');

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

function checkRequirements() {
    log('📋 Sistem gereksinimleri kontrol ediliyor...', 'blue');
    
    // Node.js kontrolü
    try {
        const nodeVersion = process.version;
        log(`✅ Node.js: ${nodeVersion}`, 'green');
    } catch (e) {
        log('❌ Node.js bulunamadı!', 'red');
        process.exit(1);
    }
    
    // Python kontrolü
    try {
        const python = spawn.sync('python', ['--version'], { encoding: 'utf8' });
        if (python.status === 0) {
            log(`✅ Python: ${python.stdout.trim()}`, 'green');
        } else {
            throw new Error('Python bulunamadı');
        }
    } catch (e) {
        log('❌ Python bulunamadı!', 'red');
        process.exit(1);
    }
    
    // Ollama kontrolü
    try {
        const ollama = spawn.sync('ollama', ['--version'], { encoding: 'utf8' });
        if (ollama.status === 0) {
            log(`✅ Ollama: ${ollama.stdout.trim()}`, 'green');
        } else {
            throw new Error('Ollama bulunamadı');
        }
    } catch (e) {
        log('❌ Ollama bulunamadı! Lütfen https://ollama.ai adresinden indirin.', 'red');
        process.exit(1);
    }
    
    console.log();
}

function checkEnvFile() {
    const envPath = path.join(__dirname, '..', 'backend', '.env');
    if (!fs.existsSync(envPath)) {
        log('⚠️  .env dosyası bulunamadı, oluşturuluyor...', 'yellow');
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
    }
}

async function startOllama() {
    return new Promise((resolve) => {
        log('🦙 Ollama servisi başlatılıyor...', 'magenta');
        
        // Ollama zaten çalışıyor mu kontrol et
        const checkOllama = spawn.sync('curl', ['-s', 'http://localhost:11434/api/tags'], { encoding: 'utf8' });
        if (checkOllama.status === 0) {
            log('✅ Ollama zaten çalışıyor', 'green');
            return resolve();
        }
        
        // Ollama'yı başlat
        const ollamaProcess = spawn('ollama', ['serve'], {
            detached: true,
            stdio: 'ignore'
        });
        
        ollamaProcess.unref();
        
        // Birkaç saniye bekle
        setTimeout(() => {
            log('✅ Ollama servisi başlatıldı', 'green');
            resolve();
        }, 3000);
    });
}

async function startBackend() {
    return new Promise((resolve) => {
        log('⚙️  Backend (FastAPI) başlatılıyor...', 'blue');
        
        const backendProcess = spawn('python', ['-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8001', '--reload'], {
            cwd: path.join(__dirname, '..', 'backend'),
            detached: true,
            stdio: 'ignore'
        });
        
        backendProcess.unref();
        
        setTimeout(() => {
            log('✅ Backend http://127.0.0.1:8001 adresinde çalışıyor', 'green');
            resolve();
        }, 5000);
    });
}

async function startFrontend() {
    return new Promise((resolve) => {
        log('🎨 Frontend (React) başlatılıyor...', 'cyan');
        
        const frontendProcess = spawn('npm', ['start'], {
            cwd: path.join(__dirname, '..', 'frontend'),
            detached: true,
            stdio: 'ignore',
            shell: true
        });
        
        frontendProcess.unref();
        
        setTimeout(() => {
            log('✅ Frontend http://localhost:3000 adresinde çalışıyor', 'green');
            resolve();
        }, 10000);
    });
}

async function main() {
    try {
        checkRequirements();
        checkEnvFile();
        
        log('🔄 Servisler sırayla başlatılıyor...\n', 'yellow');
        
        await startOllama();
        await startBackend();
        await startFrontend();
        
        console.log();
        log('🎉 Tüm servisler başarıyla başlatıldı!', 'green');
        log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'green');
        log('🌐 Frontend:  http://localhost:3000', 'cyan');
        log('⚙️  Backend:   http://127.0.0.1:8001', 'blue');
        log('🦙 Ollama:    http://localhost:11434', 'magenta');
        log('📚 API Docs:  http://127.0.0.1:8001/docs', 'blue');
        log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'green');
        console.log();
        log('💡 Durdurmak için: npm run stop', 'yellow');
        log('📊 Durum kontrol: npm run status', 'yellow');
        
    } catch (error) {
        log(`❌ Hata: ${error.message}`, 'red');
        process.exit(1);
    }
}

main();

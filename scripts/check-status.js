#!/usr/bin/env node

const { spawn } = require('cross-spawn');
const http = require('http');

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

function checkService(url, name, color) {
    return new Promise((resolve) => {
        const urlObj = new URL(url);
        const options = {
            hostname: urlObj.hostname,
            port: urlObj.port,
            path: urlObj.pathname,
            method: 'GET',
            timeout: 3000
        };

        const req = http.request(options, (res) => {
            if (res.statusCode === 200) {
                log(`✅ ${name}: ÇALIŞIYOR`, color);
                resolve({ name, status: 'running', url });
            } else {
                log(`⚠️  ${name}: HATA (${res.statusCode})`, 'yellow');
                resolve({ name, status: 'error', url });
            }
        });

        req.on('error', () => {
            log(`❌ ${name}: DURMUŞ`, 'red');
            resolve({ name, status: 'stopped', url });
        });

        req.on('timeout', () => {
            log(`⏱️  ${name}: ZAMAN AŞIMI`, 'yellow');
            resolve({ name, status: 'timeout', url });
        });

        req.end();
    });
}

async function checkAllServices() {
    log('📊 AI Ruleset Generator Durum Kontrolü\n', 'blue');
    log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'blue');

    const services = [
        { url: 'http://localhost:3000', name: 'Frontend (React)', color: 'cyan' },
        { url: 'http://127.0.0.1:8001/health', name: 'Backend (FastAPI)', color: 'blue' },
        { url: 'http://localhost:11434/api/tags', name: 'Ollama AI', color: 'magenta' }
    ];

    const results = await Promise.all(
        services.map(service => checkService(service.url, service.name, service.color))
    );

    console.log();
    log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'blue');

    const running = results.filter(r => r.status === 'running');
    const stopped = results.filter(r => r.status === 'stopped' || r.status === 'error' || r.status === 'timeout');

    if (running.length === 3) {
        log('🎉 Tüm servisler çalışıyor!', 'green');
        log('🌐 Web uygulaması: http://localhost:3000', 'cyan');
    } else if (running.length > 0) {
        log(`⚠️  ${running.length}/3 servis çalışıyor`, 'yellow');
        log('🔄 Eksik servisleri başlatmak için: npm start', 'blue');
    } else {
        log('❌ Hiçbir servis çalışmıyor', 'red');
        log('🚀 Tüm servisleri başlatmak için: npm start', 'blue');
    }

    console.log();

    // Sistem bilgileri
    log('💻 Sistem Bilgileri:', 'blue');
    try {
        const nodeVersion = process.version;
        log(`   Node.js: ${nodeVersion}`, 'green');
    } catch (e) {
        log('   Node.js: Bulunamadı', 'red');
    }

    try {
        const python = spawn.sync('python', ['--version'], { encoding: 'utf8' });
        if (python.status === 0) {
            log(`   Python: ${python.stdout.trim()}`, 'green');
        }
    } catch (e) {
        log('   Python: Bulunamadı', 'red');
    }

    try {
        const ollama = spawn.sync('ollama', ['--version'], { encoding: 'utf8' });
        if (ollama.status === 0) {
            log(`   Ollama: ${ollama.stdout.trim()}`, 'green');
        }
    } catch (e) {
        log('   Ollama: Bulunamadı', 'red');
    }

    // Ollama modelleri
    try {
        const models = spawn.sync('ollama', ['list'], { encoding: 'utf8' });
        if (models.status === 0) {
            const modelLines = models.stdout.split('\n').slice(1).filter(line => line.trim());
            if (modelLines.length > 0) {
                log('🦙 Yüklü Ollama Modelleri:', 'magenta');
                modelLines.forEach(line => {
                    const modelName = line.split(/\s+/)[0];
                    if (modelName) log(`   ${modelName}`, 'green');
                });
            }
        }
    } catch (e) {
        // Silent fail
    }

    console.log();
    log('📋 Kullanılabilir Komutlar:', 'blue');
    log('   npm start    - Tüm servisleri başlat', 'cyan');
    log('   npm stop     - Tüm servisleri durdur', 'cyan');
    log('   npm run status - Durum kontrolü', 'cyan');
    log('   npm run setup  - İlk kurulum', 'cyan');
}

checkAllServices().catch(error => {
    log(`❌ Hata: ${error.message}`, 'red');
    process.exit(1);
});

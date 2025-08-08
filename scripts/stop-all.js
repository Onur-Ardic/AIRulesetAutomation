#!/usr/bin/env node

const { spawn } = require('cross-spawn');
const path = require('path');

// Renkli console output için
const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

async function stopServices() {
    log('🛑 AI Ruleset Generator servisleri durduruluyor...\n', 'yellow');
    
    // Port tabanlı processleri öldür
    const ports = [3000, 8001, 11434];
    
    for (const port of ports) {
        try {
            log(`🔍 Port ${port} kontrol ediliyor...`, 'blue');
            
            // Windows için netstat kullan
            const netstat = spawn.sync('netstat', ['-ano'], { encoding: 'utf8' });
            if (netstat.status === 0) {
                const lines = netstat.stdout.split('\n');
                const portLine = lines.find(line => line.includes(`:${port} `));
                
                if (portLine) {
                    const parts = portLine.trim().split(/\s+/);
                    const pid = parts[parts.length - 1];
                    
                    if (pid && pid !== '0') {
                        log(`🎯 Port ${port} PID ${pid} sonlandırılıyor...`, 'yellow');
                        spawn.sync('taskkill', ['/F', '/PID', pid]);
                        log(`✅ Port ${port} temizlendi`, 'green');
                    }
                } else {
                    log(`ℹ️  Port ${port} zaten boş`, 'blue');
                }
            }
        } catch (error) {
            log(`⚠️  Port ${port} temizlenirken hata: ${error.message}`, 'yellow');
        }
    }
    
    // Node processleri için
    try {
        log('🔍 Node.js processleri kontrol ediliyor...', 'blue');
        const tasklist = spawn.sync('tasklist', ['/FI', 'IMAGENAME eq node.exe', '/FO', 'CSV'], { encoding: 'utf8' });
        if (tasklist.status === 0 && tasklist.stdout.includes('node.exe')) {
            spawn.sync('taskkill', ['/F', '/IM', 'node.exe']);
            log('✅ Node.js processleri temizlendi', 'green');
        }
    } catch (error) {
        log(`⚠️  Node processleri temizlenirken hata: ${error.message}`, 'yellow');
    }
    
    // Python processleri için
    try {
        log('🔍 Python processleri kontrol ediliyor...', 'blue');
        const tasklist = spawn.sync('tasklist', ['/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'], { encoding: 'utf8' });
        if (tasklist.status === 0 && tasklist.stdout.includes('uvicorn')) {
            spawn.sync('taskkill', ['/F', '/IM', 'python.exe']);
            log('✅ Python processleri temizlendi', 'green');
        }
    } catch (error) {
        log(`⚠️  Python processleri temizlenirken hata: ${error.message}`, 'yellow');
    }
    
    console.log();
    log('🎉 Tüm servisler başarıyla durduruldu!', 'green');
    log('🔄 Yeniden başlatmak için: npm start', 'blue');
}

stopServices().catch(error => {
    log(`❌ Hata: ${error.message}`, 'red');
    process.exit(1);
});

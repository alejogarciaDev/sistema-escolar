# =============================================
# run.ps1 - Inicia TODO el sistema (local + túnel)
# Uso: .\run.ps1
# =============================================

$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$BACKEND = Join-Path $ROOT "backend"
$FRONTEND = Join-Path $ROOT "frontend\web_tecnica"
$CONFIG = Join-Path $ROOT "js\config.js"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Iniciando Sistema Escolar + Túnel" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# ──────────────────────────────
# 0. Pasar config.js a modo túnel
# ──────────────────────────────
Write-Host "[0/4] Configurando URLs para tunnel (auraassistant.site)..." -ForegroundColor Yellow
(Get-Content $CONFIG -Raw) -replace '(?s)window\.API_AUTH = "http://192\.168\.1\.37:8001".*?window\.API = "http://192\.168\.1\.37:8002"', 'window.API_AUTH = "https://api.auraassistant.site"
window.API = "https://campus.auraassistant.site"' | Set-Content $CONFIG

# ──────────────────────────────
# 1. Servicio Central (puerto 8001)
# ──────────────────────────────
Write-Host "[1/4] Iniciando Servicio Central (auth, users, pañol) → 8001..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit cd '$BACKEND'; python -m uvicorn app.main:app --host 0.0.0.0 --port 8001" -WindowStyle Minimized
Start-Sleep -Seconds 4

# ──────────────────────────────
# 2. Servicio Campus Virtual (puerto 8002)
# ──────────────────────────────
Write-Host "[2/4] Iniciando Campus Virtual (tareas, docs) → 8002..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit cd '$BACKEND'; python -m uvicorn run_campus:app --host 0.0.0.0 --port 8002" -WindowStyle Minimized
Start-Sleep -Seconds 4

# ──────────────────────────────
# 3. Frontend (puerto 3000)
# ──────────────────────────────
Write-Host "[3/4] Iniciando Frontend (Express) → 3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit cd '$FRONTEND'; node app.js" -WindowStyle Minimized
Start-Sleep -Seconds 3

# ──────────────────────────────
# 4. Túnel Cloudflare
# ──────────────────────────────
Write-Host "[4/4] Iniciando túnel Cloudflare (auraassistant.site)..." -ForegroundColor Yellow
$cfd = "C:\Users\Admin\AppData\Local\Microsoft\WinGet\Packages\Cloudflare.cloudflared_Microsoft.Winget.Source_8wekyb3d8bbwe\cloudflared.exe"
Start-Process -WindowStyle Minimized -FilePath $cfd -ArgumentList "tunnel --config $env:USERPROFILE\.cloudflared\config-aura-prod.yml run"

Start-Sleep -Seconds 5

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  TODO ACTIVO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Sitio:        https://auraassistant.site" -ForegroundColor Green
Write-Host "  API Central:  https://api.auraassistant.site" -ForegroundColor Green
Write-Host "  API Campus:   https://campus.auraassistant.site" -ForegroundColor Green
Write-Host "  Login:        https://auraassistant.site/sistema/login.html" -ForegroundColor Green
Write-Host ""
Write-Host "  Para DETENER:  .\stop.ps1" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green

Read-Host "`nPresioná ENTER para cerrar (los servicios siguen corriendo)"

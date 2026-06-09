# stop.ps1 - Mata todos los procesos
Write-Host "Deteniendo servicios..." -ForegroundColor Yellow
Get-Process -Name "python", "node", "cloudflared" -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "Listo." -ForegroundColor Green

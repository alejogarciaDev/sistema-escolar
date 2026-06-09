@echo off
title Sistema Escolar
cd /d "%~dp0"

echo ========================================
echo   Iniciando Sistema Escolar (3 ventanas)
echo ========================================

:: 1. Servicio Central (puerto 8001)
echo [1/3] Iniciando Servicio Central → 8001...
start "Servicio Central" cmd /c "cd /d "%~dp0backend" && python -m uvicorn app.main:app --host 0.0.0.0 --port 8001"
timeout /t 4 /nobreak >nul

:: 2. Campus Virtual (puerto 8002)
echo [2/3] Iniciando Campus Virtual → 8002...
start "Campus Virtual" cmd /c "cd /d "%~dp0backend" && python -m uvicorn run_campus:app --host 0.0.0.0 --port 8002"
timeout /t 4 /nobreak >nul

:: 3. Frontend (puerto 3000)
echo [3/3] Iniciando Frontend Web → 3000...
start "Frontend" cmd /c "cd /d "%~dp0frontend\web_tecnica" && node app.js"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo  TODO ACTIVO
echo ========================================
echo  Frontend:  http://localhost:3000
echo  Login:     http://localhost:3000/sistema/login.html
echo.
echo  Para cerrar: cerrá las ventanas individualmente
echo ========================================
pause

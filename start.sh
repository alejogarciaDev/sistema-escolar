#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend/web_tecnica"

echo "========================================"
echo "  Iniciando Sistema Escolar"
echo "========================================"
echo "  Backend Central:  http://0.0.0.0:8001"
echo "  Backend Campus:   http://0.0.0.0:8002"
echo "  Frontend Web:     http://0.0.0.0:3000"
echo "  Login:            http://localhost:3000/sistema/login.html"
echo "========================================"

cleanup() {
    echo ""
    echo "Deteniendo servicios..."
    kill $PID_CENTRAL $PID_CAMPUS $PID_FRONTEND 2>/dev/null
    wait
    echo "Todo detenido."
}
trap cleanup EXIT INT TERM

# Activar venv
source "$BACKEND_DIR/venv/bin/activate"

# 1. Servicio Central (puerto 8001)
cd "$BACKEND_DIR"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 &
PID_CENTRAL=$!

# 2. Campus Virtual (puerto 8002)
python -m uvicorn run_campus:app --host 0.0.0.0 --port 8002 &
PID_CAMPUS=$!

# 3. Frontend (puerto 3000)
cd "$FRONTEND_DIR"
node app.js &
PID_FRONTEND=$!

echo ""
echo "Todos los servicios activos. Presioná Ctrl+C para detener."

wait

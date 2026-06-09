#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend/web_tecnica"
CONFIG_FILE="$HOME/.cloudflared/config-aura-prod.yml"

echo "========================================"
echo "  Iniciando Sistema Escolar + Túnel"
echo "========================================"
echo "  Sitio:        https://auraassistant.site"
echo "  API Central:  https://api.auraassistant.site"
echo "  API Campus:   https://campus.auraassistant.site"
echo "  Login:        https://auraassistant.site/sistema/login.html"
echo "========================================"

cleanup() {
    echo ""
    echo "Deteniendo servicios..."
    kill $PID_CENTRAL $PID_CAMPUS $PID_FRONTEND $PID_TUNEL 2>/dev/null
    wait
    echo "Todo detenido."
}
trap cleanup EXIT INT TERM

# Activar venv
source "$BACKEND_DIR/venv/bin/activate"

# 1. Servicio Central (puerto 8001)
echo "[1/4] Servicio Central → 8001..."
cd "$BACKEND_DIR"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 &
PID_CENTRAL=$!

# 2. Campus Virtual (puerto 8002)
echo "[2/4] Campus Virtual → 8002..."
python -m uvicorn run_campus:app --host 0.0.0.0 --port 8002 &
PID_CAMPUS=$!

# 3. Frontend (puerto 3000)
echo "[3/4] Frontend Web → 3000..."
cd "$FRONTEND_DIR"
node app.js &
PID_FRONTEND=$!

# 4. Túnel Cloudflare
sleep 3
echo "[4/4] Iniciando túnel Cloudflare..."
if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: No se encuentra $CONFIG_FILE"
    echo "Primero ejecutá: bash setup_tunnel.sh"
    exit 1
fi
cloudflared tunnel --config "$CONFIG_FILE" run &
PID_TUNEL=$!

echo ""
echo "========================================"
echo "  TODO ACTIVO"
echo "========================================"
echo "  Presioná Ctrl+C para detener todo."
echo "========================================"

wait

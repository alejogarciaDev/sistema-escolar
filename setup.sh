#!/bin/bash
set -e

echo "========================================"
echo "  Setup Sistema Escolar"
echo "========================================"

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ─── Backend ───
echo "[1/4] Instalando dependencias Python..."
cd "$ROOT_DIR/backend"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# ─── Frontend ───
echo "[2/4] Instalando dependencias Node.js..."
cd "$ROOT_DIR/frontend/web_tecnica"
npm install

# ─── Semilla DB ───
echo "[3/4] Sembrando base de datos (si está vacía)..."
cd "$ROOT_DIR/backend"
source venv/bin/activate
python seed.py 2>/dev/null || echo "  seed ya ejecutada o DB poblada"
deactivate

echo "[4/4] Setup completo."
echo ""
echo "Para iniciar:  bash start.sh"
echo "Para detener:  Ctrl+C en cada terminal (o kill)"

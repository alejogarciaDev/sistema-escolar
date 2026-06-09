#!/bin/bash
set -e

echo "========================================"
echo "  Configurar túnel Cloudflare"
echo "  para auraassistant.site"
echo "========================================"
echo ""

# ─── Login ───
echo "[1/4] Iniciando sesión en Cloudflare..."
echo "Se va a abrir un navegador. Iniciá sesión con"
echo "la cuenta que tiene auraassistant.site"
cloudflared tunnel login

# ─── Crear túnel ───
echo ""
echo "[2/4] Creando túnel 'aura-prod'..."
cloudflared tunnel create aura-prod

# Leer el ID del túnel desde los archivos
TUNNEL_ID=$(ls ~/.cloudflared/*.json 2>/dev/null | head -1 | xargs -I{} basename {} .json)
if [ -z "$TUNNEL_ID" ]; then
    echo "ERROR: No se encontró el archivo de credenciales. Revisá ~/.cloudflared/"
    exit 1
fi
echo "  Túnel ID: $TUNNEL_ID"

# ─── Rutas DNS ───
echo ""
echo "[3/4] Creando rutas DNS..."
cloudflared tunnel route dns aura-prod auraassistant.site
cloudflared tunnel route dns aura-prod api.auraassistant.site
cloudflared tunnel route dns aura-prod campus.auraassistant.site

# ─── Config.yml ───
echo ""
echo "[4/4] Generando config.yml..."
mkdir -p ~/.cloudflared
cat > ~/.cloudflared/config-aura-prod.yml << EOF
tunnel: $TUNNEL_ID
credentials-file: /home/vboxuser/.cloudflared/$TUNNEL_ID.json

ingress:
  - hostname: auraassistant.site
    service: http://localhost:3000
  - hostname: api.auraassistant.site
    service: http://localhost:8001
  - hostname: campus.auraassistant.site
    service: http://localhost:8002
  - service: http_status:404
EOF

echo ""
echo "========================================"
echo "  Configuración completa."
echo "========================================"
echo "  Para iniciar todo:"
echo "    bash start.sh"
echo "    cloudflared tunnel --config ~/.cloudflared/config-aura-prod.yml run"
echo ""
echo "  O usar:"
echo "    bash start_tunnel.sh"
echo "========================================"

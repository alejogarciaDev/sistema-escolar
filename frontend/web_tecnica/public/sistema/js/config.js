// =============================================
// config.js - Configuración centralizada
// =============================================
// Cambiá las URLs según corresponda:
//   - Modo LOCAL: usá las URLs con IP local
//   - Modo TUNEL: comentá las locales y
//     descomentá las de auraassistant.site
// =============================================

// ─── MODO LOCAL (desarrollo / red local) ───
window.API_AUTH = "http://127.0.0.1:8001"
window.API = "http://127.0.0.1:8002";

// ─── MODO TÚNEL (Cloudflare → auraassistant.site) ───
// Descomentar estas líneas y comentar las de arriba
// cuando el túnel esté corriendo:
// window.API_AUTH = "https://api.auraassistant.site";
// window.API = "https://campus.auraassistant.site";



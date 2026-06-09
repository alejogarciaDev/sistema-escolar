// =============================================
// config.js - Configuración centralizada
// =============================================
// Cambiá las URLs según corresponda:
//   - Modo LOCAL: usá las URLs con IP local
//   - Modo TUNEL: comentá las locales y
//     descomentá las de auraassistant.site
// =============================================

// ─── MODO TÚNEL (Cloudflare → auraassistant.site) ───
window.API_AUTH = "https://api.auraassistant.site";
window.API = "https://campus.auraassistant.site";

// ─── MODO LOCAL (desarrollo / red local) ───
// Descomentar estas líneas y comentar las de arriba
// cuando NO uses el túnel:
// window.API_AUTH = "https://api.auraassistant.site"
window.API = "https://campus.auraassistant.site";



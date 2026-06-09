import os

# 📁 Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 📂 Carpeta de archivos (legajos, documentos, etc)
# 👉 Usa variable de entorno si existe, sino usa carpeta local
FILES_PATH = os.getenv(
    "FILES_PATH",
    os.path.join(BASE_DIR, "legajos")  # default dentro del proyecto
)

# 🔐 Seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta")

# 🌍 Entorno (opcional pero PRO)
ENV = os.getenv("ENV", "dev")  # dev / prod

# 📏 Tamaño máximo de archivo (opcional)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# 📦 Tipos permitidos (opcional)
ALLOWED_TYPES = ["application/pdf", "image/jpeg", "image/png"]

# 🛠 Crear carpeta automáticamente si no existe
os.makedirs(FILES_PATH, exist_ok=True)


# =========================================================
# 🔧 COMANDO PARA CAMBIAR LA RUTA DE ARCHIVOS (IMPORTANTE)
# =========================================================
# En Linux / servidor:
# export FILES_PATH=/mnt/archivos/legajos
#
# En .env:
# FILES_PATH=/mnt/archivos/legajos
#
# Luego reiniciar el backend
# =========================================================
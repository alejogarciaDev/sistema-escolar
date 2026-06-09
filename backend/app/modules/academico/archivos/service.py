import os
from sqlalchemy.orm import Session
from datetime import datetime

from .models import Archivo
from app.core.config import FILES_PATH


# ================= EXTENSIONES PERMITIDAS =================
EXTENSIONES_PERMITIDAS = [
    "pdf",
    "png",
    "jpg",
    "jpeg",

    # Word
    "doc",
    "docx",

    # Excel
    "xls",
    "xlsx"
]


# ================= SUBIR ARCHIVO =================
def guardar_archivo(db: Session, alumno, file):

    if not file.filename:
        raise ValueError("Archivo sin nombre")

    extension = file.filename.split(".")[-1].lower()

    # tipos permitidos
    permitidos = ["pdf", "png", "jpg", "jpeg", "doc", "docx", "xls", "xlsx"]

    if extension not in permitidos:
        raise ValueError("Tipo de archivo no permitido")

    # 📁 carpeta por alumno
    carpeta = os.path.join(FILES_PATH, str(alumno.dni))
    os.makedirs(carpeta, exist_ok=True)

    # 👇 nombre original (el que ve el usuario)
    nombre_original = file.filename

    # 👇 nombre real (único en disco)
    nombre_guardado = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{nombre_original}"

    ruta = os.path.join(carpeta, nombre_guardado)

    # guardar archivo
    with open(ruta, "wb") as buffer:
        buffer.write(file.file.read())

    # guardar en DB
    nuevo = Archivo(
        alumno_id=alumno.id,
        nombre_archivo=nombre_original,  # 👈 nombre lindo
        ruta_archivo=ruta,               # 👈 nombre real
        tipo=extension
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo

# ================= LISTAR =================
def listar_archivos(db: Session, alumno_id: int):
    archivos = db.query(Archivo).filter(Archivo.alumno_id == alumno_id).all()

    validos = []

    for a in archivos:
        if os.path.exists(a.ruta_archivo):
            validos.append(a)
        else:
            # 🔥 AUTO LIMPIEZA
            db.delete(a)

    db.commit()
    return validos


# ================= POR ID =================
def obtener_archivo_por_id(db: Session, archivo_id: int):
    return db.query(Archivo).filter(Archivo.id == archivo_id).first()
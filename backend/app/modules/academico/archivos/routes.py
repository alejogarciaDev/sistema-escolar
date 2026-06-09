from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import mimetypes

from app.core.database import get_db
from app.core.security import get_current_user
from app.modules.academico.alumnos.service import obtener_por_dni
from app.modules.academico.alumnos.models import Alumno
from app.modules.academico.materias.models import Materia
from .models import Archivo
from . import service
from .schemas import ArchivoOut

router = APIRouter(prefix="/archivos", tags=["Archivos"])


# ================= SUBIR =================
@router.post("/alumno/{dni}")
def subir_archivo(
    dni: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    alumno = obtener_por_dni(db, dni)

    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    return service.guardar_archivo(db, alumno, file)
# ================= LISTAR =================
@router.get("/alumno/{dni}", response_model=list[ArchivoOut])
def listar_archivos(dni: str, db: Session = Depends(get_db)):
    alumno = obtener_por_dni(db, dni)

    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    return service.listar_archivos(db, alumno.id)


# ================= VER =================
@router.get("/ver/{archivo_id}")
def ver_archivo(archivo_id: int, db: Session = Depends(get_db)):
    archivo = service.obtener_archivo_por_id(db, archivo_id)

    if not archivo:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    if not os.path.exists(archivo.ruta_archivo):
        db.delete(archivo)
        db.commit()
        raise HTTPException(status_code=404, detail="Archivo eliminado")

    mime_type, _ = mimetypes.guess_type(archivo.ruta_archivo)

    # 👇 tipos que el navegador puede mostrar
    inline_types = [
        "application/pdf",
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/webp"
    ]

    disposition = "inline" if mime_type in inline_types else "attachment"

    return FileResponse(
        archivo.ruta_archivo,
        media_type=mime_type or "application/octet-stream",
        headers={"Content-Disposition": disposition}
    )

# ================= DESCARGAR =================
@router.get("/descargar/{archivo_id}")
def descargar_archivo(archivo_id: int, db: Session = Depends(get_db)):
    archivo = service.obtener_archivo_por_id(db, archivo_id)

    if not archivo:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    if not os.path.exists(archivo.ruta_archivo):
        db.delete(archivo)
        db.commit()
        raise HTTPException(status_code=404, detail="Archivo eliminado del sistema")

    return FileResponse(
        archivo.ruta_archivo,
        filename=archivo.nombre_archivo,
        media_type="application/octet-stream"
    )


# ================= SUBIR CON MATERIA (FRONTEND) =================
@router.post("/subir")
def subir_archivo_con_materia(
    file: UploadFile = File(...),
    nombre_archivo: str = Form(""),
    materia_id: int = Form(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    alumno = db.query(Alumno).filter(Alumno.user_id == user["id"]).first()
    if not alumno:
        raise HTTPException(status_code=400, detail="No tienes un perfil de alumno asociado")

    archivo = service.guardar_archivo(db, alumno, file)
    if materia_id:
        archivo.materia_id = materia_id
        db.commit()
        db.refresh(archivo)

    return archivo


# ================= MIS TRABAJOS (FRONTEND) =================
@router.get("/mis-trabajos", response_model=list[ArchivoOut])
def mis_trabajos(db: Session = Depends(get_db), user=Depends(get_current_user)):
    alumno = db.query(Alumno).filter(Alumno.user_id == user["id"]).first()
    if not alumno:
        raise HTTPException(status_code=400, detail="No tienes un perfil de alumno asociado")
    return service.listar_archivos(db, alumno.id)


# ================= TRABAJOS POR MATERIA (FRONTEND PROFESOR) =================
@router.get("/materia/{materia_id}")
def trabajos_por_materia(materia_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    archivos = db.query(Archivo).filter(Archivo.materia_id == materia_id).all()
    materia = db.query(Materia).filter(Materia.id == materia_id).first()
    resultados = []
    for a in archivos:
        if not os.path.exists(a.ruta_archivo):
            db.delete(a)
            db.commit()
            continue
        alumno = db.query(Alumno).filter(Alumno.id == a.alumno_id).first()
        resultados.append({
            "id": a.id,
            "nombre_archivo": a.nombre_archivo,
            "fecha_subida": a.fecha_subida,
            "alumno_nombre": f"{alumno.nombre} {alumno.apellido}" if alumno else "Desconocido",
            "materia_nombre": materia.nombre if materia else None
        })
    return resultados
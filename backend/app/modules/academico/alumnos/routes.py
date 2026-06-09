from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_permission
from . import service, schemas

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


@router.post("/", response_model=schemas.AlumnoSimple)
def crear_alumno(data: schemas.AlumnoCreate, db: Session = Depends(get_db), _=Depends(require_permission("alumnos.create"))):
    try:
        return service.crear_alumno(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[schemas.AlumnoSimple])
def listar(db: Session = Depends(get_db), _=Depends(require_permission("alumnos.list"))):
    return service.listar_alumnos(db)


@router.get("/{dni}", response_model=schemas.AlumnoOut)
def obtener(dni: str, db: Session = Depends(get_db), _=Depends(require_permission("alumnos.list"))):
    alumno = service.obtener_por_dni(db, dni)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno


@router.put("/{dni}", response_model=schemas.AlumnoSimple)
def actualizar(dni: str, data: schemas.AlumnoUpdate, db: Session = Depends(get_db), _=Depends(require_permission("alumnos.create"))):
    alumno = service.actualizar_alumno(db, dni, data)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno


@router.delete("/{dni}")
def eliminar(dni: str, db: Session = Depends(get_db), _=Depends(require_permission("alumnos.create"))):
    alumno = service.eliminar_alumno(db, dni)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return {"msg": "eliminado"}


# ---- HISTORIAL ACADÉMICO ----

@router.get("/{dni}/historial", response_model=list[schemas.HistorialOut])
def listar_historial(dni: str, db: Session = Depends(get_db), _=Depends(require_permission("alumnos.list"))):
    alumno = service.obtener_por_dni(db, dni)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return service.listar_historial(db, alumno.id)


@router.post("/{dni}/historial", response_model=schemas.HistorialOut)
def agregar_historial(dni: str, data: schemas.HistorialCreate, db: Session = Depends(get_db), _=Depends(require_permission("alumnos.create"))):
    alumno = service.obtener_por_dni(db, dni)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    entry = service.agregar_historial(db, alumno.id, data)
    if not entry:
        raise HTTPException(status_code=400, detail="Error al crear historial")
    return entry


@router.delete("/historial/{historial_id}")
def eliminar_historial(historial_id: int, db: Session = Depends(get_db), _=Depends(require_permission("alumnos.create"))):
    entry = service.eliminar_historial(db, historial_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return {"msg": "eliminado"}

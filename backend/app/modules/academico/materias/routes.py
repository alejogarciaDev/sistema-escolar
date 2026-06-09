from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_permission
from app.modules.academico.materias.models import Materia

router = APIRouter(prefix="/materias", tags=["Materias"])

@router.get("/")
def get_materias(db: Session = Depends(get_db)):
    return db.query(Materia).all()

@router.post("/")
def create_materia(nombre: str, descripcion: str = "", db: Session = Depends(get_db), _=Depends(require_permission("materias.create"))):
    nueva = Materia(nombre=nombre, descripcion=descripcion)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

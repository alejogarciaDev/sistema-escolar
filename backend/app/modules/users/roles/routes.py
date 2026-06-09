from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_permission

from . import service, schemas

router = APIRouter(prefix="/roles", tags=["Roles"])


# =========================
# CREAR
# =========================
@router.post("/", response_model=schemas.RoleOut)
def create(role: schemas.RoleCreate, db: Session = Depends(get_db), _=Depends(require_permission("roles.create"))):
    return service.create_role(db, role.name)


# =========================
# LISTAR
# =========================
@router.get("/", response_model=list[schemas.RoleOut])
def list_roles(db: Session = Depends(get_db)):
    return service.get_roles(db)


# =========================
# OBTENER POR ID
# =========================
@router.get("/{role_id}", response_model=schemas.RoleOut)
def get_role(role_id: int, db: Session = Depends(get_db)):
    return service.get_role(db, role_id)


# =========================
# ELIMINAR
# =========================
@router.delete("/{role_id}")
def delete(role_id: int, db: Session = Depends(get_db), _=Depends(require_permission("roles.delete"))):
    return service.delete_role(db, role_id)
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_permission

from . import service, schemas

router = APIRouter(prefix="/users", tags=["Users"])


# =========================
# CREAR USUARIO
# =========================
@router.post("/", response_model=schemas.UserOut)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db), _=Depends(require_permission("users.create"))):
    return service.create_user(db, data)


# =========================
# LISTAR USUARIOS
# =========================
@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db), _=Depends(require_permission("users.list"))):
    return service.get_users(db)


# =========================
# OBTENER POR ID
# =========================
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(require_permission("users.list"))):
    return service.get_user_by_id(db, user_id)


# =========================
# ELIMINAR USUARIO
# =========================
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _=Depends(require_permission("users.delete"))):
    return service.delete_user(db, user_id)


# =========================
# CAMBIAR ROL
# =========================
@router.put("/{user_id}/role")
def change_role(user_id: int, role_id: int, db: Session = Depends(get_db), _=Depends(require_permission("users.change_role"))):
    return service.change_role(db, user_id, role_id)

@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    return service.login(db, email, password)
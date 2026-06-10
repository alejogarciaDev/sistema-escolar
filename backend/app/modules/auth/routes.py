from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_db
from app.modules.users.users.service import get_user_by_email
from app.core.security import create_access_token, get_current_user_db

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# SCHEMA LOGIN (FRONTEND)
# =========================
class LoginRequest(BaseModel):
    email: str
    password: str


# =========================
# LOGIN NORMAL (TU APP)
# =========================
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = get_user_by_email(db, data.email)

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if user.password != data.password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    role_name = user.role.name if user.role else None

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role_id,
        "role_name": role_name
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role_id,
            "role_name": role_name
        }
    }


# =========================
# TOKEN (SWAGGER / OAUTH2)
# =========================
@router.post("/token")
def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # ⚠️ Swagger usa "username"
    user = get_user_by_email(db, form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    role_name = user.role.name if user.role else None

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role_id,
        "role_name": role_name
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# MAPA DE DASHBOARDS
# =========================
DASHBOARDS = [
    {"id": "admin",     "label": "Panel Admin",        "url": "dashboard_admin.html",     "roles": [3], "permissions": ["dashboard.admin"]},
    {"id": "profesor",  "label": "Panel Profesor",      "url": "dashboard_profesor.html",  "roles": [5], "permissions": ["dashboard.profesor"]},
    {"id": "alumno",    "label": "Panel Alumno",        "url": "dashboard_alumno.html",    "roles": [4], "permissions": ["dashboard.alumno"]},
    {"id": "panol",     "label": "Panel Pañol",         "url": "dashboard_panol2.html",     "roles": [2], "permissions": ["dashboard.panol"]},
    {"id": "ofalumnos", "label": "Panel Oficina Alumnos","url": "dashboard_ofalumnos.html", "roles": [1], "permissions": ["dashboard.ofalumnos"]},
]


# =========================
# MIS DASHBOARDS
# =========================
@router.get("/mis-dashboards")
def mis_dashboards(user=Depends(get_current_user_db)):
    role_perms = {p.name for p in user.role.permissions} if user.role else set()
    user_perms = {p.name for p in user.permissions}
    all_perms = role_perms | user_perms

    accesibles = []
    for d in DASHBOARDS:
        if user.role_id in d["roles"]:
            accesibles.append(d)
        elif any(p in all_perms for p in d["permissions"]):
            accesibles.append(d)

    return accesibles
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.users.users.models import User

# =========================
# CONFIG JWT
# =========================
SECRET_KEY = "clave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# =========================
# CREAR TOKEN
# =========================
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# =========================
# USER ACTUAL (desde JWT, sin DB)
# =========================
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role_id = payload.get("role")
        role_name = payload.get("role_name")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return {
            "id": int(user_id),
            "role": role_id,
            "role_name": role_name
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


# =========================
# USER DESDE DB (con permisos)
# =========================
def get_current_user_db(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        user = db.query(User).filter(User.id == int(user_id)).first()

        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


# =========================
# PERMISSION CHECKER
# =========================
def require_permission(permission_name: str):
    def permission_checker(user: User = Depends(get_current_user_db)):
        role_perms = {p.name for p in user.role.permissions} if user.role else set()
        user_perms = {p.name for p in user.permissions}
        all_perms = role_perms | user_perms

        if permission_name not in all_perms:
            raise HTTPException(
                status_code=403,
                detail=f"No autorizado. Se requiere permiso: {permission_name}"
            )
        return user
    return permission_checker


# =========================
# ROLE CHECKER
# =========================
def require_role(role_name: str):
    def role_checker(user: User = Depends(get_current_user_db)):
        if user.role is None or user.role.name != role_name:
            raise HTTPException(
                status_code=403,
                detail=f"No autorizado. Se requiere rol: {role_name}"
            )
        return user
    return role_checker


# =========================
# SOLO ADMIN (mantiene compatibilidad)
# =========================
def require_admin(user=Depends(get_current_user_db)):
    if user.role is None or user.role.name != "admin":
        raise HTTPException(status_code=403, detail="No autorizado (solo admin)")
    return user

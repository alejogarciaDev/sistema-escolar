# app/modules/panol/core.py

from datetime import datetime, timedelta
import hashlib
from jose import jwt, JWTError

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import User

# -----------------------------
# JWT CONFIG
# -----------------------------
SECRET_KEY = "SECRET_SUPER_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# -----------------------------
# TOKEN
# -----------------------------
def create_access_token_local(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=60))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain, hashed):
    return hashlib.sha256(plain.encode()).hexdigest() == hashed


# -----------------------------
# USER AUTH
# -----------------------------
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User)\
        .options(joinedload(User.role))\
        .filter(User.email == email)\
        .first()

    if not user:
        raise credentials_exception

    return user


# -----------------------------
# ROLES
# -----------------------------
def admin_required(user=Depends(get_current_user)):
    if not user.role or user.role.name != "admin":
        raise HTTPException(403, "Solo admin")
    return user


def admin_or_panol(user=Depends(get_current_user)):
    if not user.role or user.role.name not in ["admin", "panol"]:
        raise HTTPException(403, "Solo admin o pañol")
    return user
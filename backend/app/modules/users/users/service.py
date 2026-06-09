from sqlalchemy.orm import Session
from fastapi import HTTPException

from .models import User

def create_user(db: Session, data):
    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise HTTPException(400, "El email ya está registrado")

    new_user = User(
        name=data.name,
        email=data.email,
        password=data.password,
        role_id=data.role_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
# =========================
# OBTENER POR EMAIL (LOGIN)
# =========================
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# =========================
# LOGIN
# =========================
def login(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    if user.password != password:
        raise HTTPException(401, "Contraseña incorrecta")

    return {
        "message": "Login exitoso",
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "role_id": user.role_id
    }

def get_users(db: Session):
    return db.query(User).all()
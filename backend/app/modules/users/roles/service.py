from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Role


# =========================
# CREAR ROL
# =========================
def create_role(db: Session, name: str):
    existing = db.query(Role).filter(Role.name == name).first()
    if existing:
        raise HTTPException(400, "El rol ya existe")

    role = Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


# =========================
# LISTAR ROLES
# =========================
def get_roles(db: Session):
    return db.query(Role).all()


# =========================
# OBTENER ROL POR ID
# =========================
def get_role(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(404, "Rol no encontrado")

    return role


# =========================
# ELIMINAR ROL
# =========================
def delete_role(db: Session, role_id: int):
    role = get_role(db, role_id)

    db.delete(role)
    db.commit()

    return {"message": "Rol eliminado"}


# =========================
# ASIGNAR PERMISO A ROL
# =========================
def add_permission(db: Session, role_id: int, permission):
    role = get_role(db, role_id)

    if permission not in role.permissions:
        role.permissions.append(permission)

    db.commit()
    db.refresh(role)

    return role


# =========================
# QUITAR PERMISO
# =========================
def remove_permission(db: Session, role_id: int, permission):
    role = get_role(db, role_id)

    if permission in role.permissions:
        role.permissions.remove(permission)
        db.commit()
        db.refresh(role)

    return role
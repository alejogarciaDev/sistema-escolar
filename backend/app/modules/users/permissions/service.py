from sqlalchemy.orm import Session
from fastapi import HTTPException

from .models import Permission
from app.modules.users.roles.models import Role
from app.modules.users.users.models import User


def create_permission(db: Session, name: str):
    existing = db.query(Permission).filter_by(name=name).first()
    if existing:
        raise HTTPException(400, "El permiso ya existe")

    perm = Permission(name=name)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm


def get_permissions(db: Session):
    return db.query(Permission).all()


def get_user_permissions(db: Session, user_id: int):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    user_perm_names = {p.name for p in user.permissions}
    role_perm_names = {p.name for p in user.role.permissions} if user.role else set()

    return {
        "user_id": user.id,
        "role_permissions": list(role_perm_names),
        "extra_permissions": list(user_perm_names),
        "all_permissions": list(role_perm_names | user_perm_names)
    }


def assign_permission_to_role(db: Session, role_id: int, permission_id: int):
    role = db.query(Role).get(role_id)
    if not role:
        raise HTTPException(404, "Rol no encontrado")

    perm = db.query(Permission).get(permission_id)
    if not perm:
        raise HTTPException(404, "Permiso no encontrado")

    role.permissions.append(perm)
    db.commit()

    return {"message": "Permiso asignado al rol"}


def assign_permission_to_user(db: Session, user_id: int, permission_id: int):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    perm = db.query(Permission).get(permission_id)
    if not perm:
        raise HTTPException(404, "Permiso no encontrado")

    if perm in user.permissions:
        raise HTTPException(400, "El usuario ya tiene este permiso")

    user.permissions.append(perm)
    db.commit()

    return {"message": "Permiso asignado al usuario"}


def remove_permission_from_user(db: Session, user_id: int, permission_id: int):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    perm = db.query(Permission).get(permission_id)
    if not perm:
        raise HTTPException(404, "Permiso no encontrado")

    if perm not in user.permissions:
        raise HTTPException(400, "El usuario no tiene este permiso")

    user.permissions.remove(perm)
    db.commit()

    return {"message": "Permiso removido del usuario"}

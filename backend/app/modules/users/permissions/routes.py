from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_permission
from . import service, schemas

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.post("/", response_model=schemas.PermissionOut)
def create(permission: schemas.PermissionCreate, db: Session = Depends(get_db), _=Depends(require_permission("permissions.create"))):
    return service.create_permission(db, permission.name)


@router.get("/", response_model=list[schemas.PermissionOut])
def list_permissions(db: Session = Depends(get_db)):
    return service.get_permissions(db)


@router.post("/assign-role")
def assign_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db), _=Depends(require_permission("permissions.assign"))):
    return service.assign_permission_to_role(db, role_id, permission_id)


@router.post("/assign-user")
def assign_to_user(user_id: int, permission_id: int, db: Session = Depends(get_db), _=Depends(require_permission("permissions.assign"))):
    return service.assign_permission_to_user(db, user_id, permission_id)


@router.delete("/assign-user")
def remove_from_user(user_id: int, permission_id: int, db: Session = Depends(get_db), _=Depends(require_permission("permissions.assign"))):
    return service.remove_permission_from_user(db, user_id, permission_id)


@router.get("/user/{user_id}")
def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    return service.get_user_permissions(db, user_id)

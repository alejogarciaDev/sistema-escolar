from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Role

def create_initial_roles():
    db: Session = SessionLocal()

    roles = ["admin", "user", "superadmin", "panol", "profesor", "alumno"]

    for role_name in roles:
        existing = db.query(Role).filter(Role.name == role_name).first()
        if not existing:
            new_role = Role(name=role_name)
            db.add(new_role)

    db.commit()
    db.close()

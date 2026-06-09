import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import Base, engine, SessionLocal
from app.core.models import *
from app.modules.users.roles.service import create_role
from app.modules.users.users.service import create_user
from app.modules.academico.materias.models import Materia
from app.modules.academico.alumnos.models import Alumno
from app.modules.users.permissions.models import Permission

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    existing = db.query(Materia).count()
    if existing > 0:
        print("Ya hay datos, no se seedea")
        db.close()
        exit(0)

    # Roles en orden: 1=oficina_alumnos, 2=panol, 3=admin, 4=alumno, 5=profesor
    from app.modules.users.roles.models import Role
    for name in ["oficina_alumnos", "panol", "admin", "alumno", "profesor"]:
        r = Role(name=name)
        db.add(r)
    db.commit()

    # =========================
    # PERMISOS
    # =========================
    all_permissions = [
        "users.create", "users.list", "users.delete", "users.change_role",
        "roles.create", "roles.delete",
        "permissions.create", "permissions.assign",
        "tareas.create", "tareas.edit", "tareas.delete",
        "entregas.ver_todas", "entregas.calificar",
        "materiales.create", "materiales.delete",
        "compartidos.create", "compartidos.delete",
        "alumnos.create", "alumnos.list",
        "materias.create",
    ]
    perm_objects = {}
    for name in all_permissions:
        p = Permission(name=name)
        db.add(p)
        perm_objects[name] = p
    db.commit()

    # Refrescar para tener IDs
    for name in all_permissions:
        db.refresh(perm_objects[name])

    # =========================
    # ASIGNAR PERMISOS A ROLES
    # =========================
    roles = {r.name: r for r in db.query(Role).all()}

    # Admin → todos los permisos
    for p in perm_objects.values():
        roles["admin"].permissions.append(p)

    # Profesor → permisos de campus + alumnos.list + materias.create
    profesor_perms = [
        "tareas.create", "tareas.edit", "tareas.delete",
        "entregas.ver_todas", "entregas.calificar",
        "materiales.create", "materiales.delete",
        "compartidos.create", "compartidos.delete",
        "alumnos.list",
        "materias.create",
    ]
    for name in profesor_perms:
        roles["profesor"].permissions.append(perm_objects[name])

    # Oficina Alumnos → alumnos + users.list
    oficina_perms = ["alumnos.create", "alumnos.list", "users.list"]
    for name in oficina_perms:
        roles["oficina_alumnos"].permissions.append(perm_objects[name])

    db.commit()

    # Users
    from app.modules.users.users.schemas import UserCreate
    u1 = UserCreate(name="Juan Perez", email="juan@test.com", password="123", role_id=4)
    create_user(db, u1)

    u2 = UserCreate(name="Carlos Profe", email="profe@test.com", password="123", role_id=5)
    create_user(db, u2)

    # Materias
    db.add(Materia(nombre="Matematicas", descripcion="Matematicas Aplicadas"))
    db.add(Materia(nombre="Lengua", descripcion="Literatura"))
    db.commit()

    # Alumno
    db.add(Alumno(dni="12345678", nombre="Juan", apellido="Perez", user_id=1))
    db.commit()

    print("Seed completado correctamente")
    print("Roles:", {r.name: r.id for r in db.query(Role).all()})
    print("Users:", [(u.id, u.name, u.role_id) for u in db.query(User).all()])

except Exception as e:
    db.rollback()
    print("Error:", e)
    raise
finally:
    db.close()

from sqlalchemy.orm import Session
from .models import Alumno


# 🔹 Crear alumno
def crear_alumno(db: Session, dni: str, nombre: str, apellido: str):
    # verificar si ya existe
    existente = db.query(Alumno).filter(Alumno.dni == dni).first()
    if existente:
        raise ValueError("El alumno ya existe")

    nuevo = Alumno(
        dni=dni,
        nombre=nombre,
        apellido=apellido
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# 🔹 Buscar por DNI (CLAVE para todo el sistema)
def obtener_por_dni(db: Session, dni: str):
    return db.query(Alumno).filter(Alumno.dni == dni).first()


# 🔹 Listar alumnos
def listar_alumnos(db: Session):
    return db.query(Alumno).all()


# 🔹 Eliminar alumno
def eliminar_alumno(db: Session, dni: str):
    alumno = obtener_por_dni(db, dni)

    if not alumno:
        return None

    db.delete(alumno)
    db.commit()

    return alumno
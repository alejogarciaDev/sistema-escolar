from sqlalchemy.orm import Session
from .models import Alumno, AlumnoHistorial


def crear_alumno(db: Session, data):
    existente = db.query(Alumno).filter(Alumno.dni == data.dni).first()
    if existente:
        raise ValueError("El alumno ya existe")

    alumno = Alumno(
        dni=data.dni,
        nombre=data.nombre,
        apellido=data.apellido
    )

    db.add(alumno)
    db.commit()
    db.refresh(alumno)

    return alumno


def actualizar_alumno(db: Session, dni: str, data):
    alumno = db.query(Alumno).filter(Alumno.dni == dni).first()
    if not alumno:
        return None

    if data.nombre is not None:
        alumno.nombre = data.nombre
    if data.apellido is not None:
        alumno.apellido = data.apellido
    if data.folio is not None:
        alumno.folio = data.folio
    if data.legajo is not None:
        alumno.legajo = data.legajo

    db.commit()
    db.refresh(alumno)
    return alumno


def obtener_por_dni(db: Session, dni: str):
    return db.query(Alumno).filter(Alumno.dni == dni).first()


def obtener_por_id(db: Session, alumno_id: int):
    return db.query(Alumno).filter(Alumno.id == alumno_id).first()


def listar_alumnos(db: Session):
    return db.query(Alumno).all()


def eliminar_alumno(db: Session, dni: str):
    alumno = obtener_por_dni(db, dni)
    if not alumno:
        return None
    db.delete(alumno)
    db.commit()
    return alumno


def agregar_historial(db: Session, alumno_id: int, data):
    alumno = db.query(Alumno).filter(Alumno.id == alumno_id).first()
    if not alumno:
        return None

    entry = AlumnoHistorial(
        alumno_id=alumno_id,
        anio=data.anio,
        curso=data.curso,
        repitio=data.repitio,
        observaciones=data.observaciones
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def eliminar_historial(db: Session, historial_id: int):
    entry = db.query(AlumnoHistorial).filter(AlumnoHistorial.id == historial_id).first()
    if not entry:
        return None
    db.delete(entry)
    db.commit()
    return entry


def listar_historial(db: Session, alumno_id: int):
    return db.query(AlumnoHistorial).filter(AlumnoHistorial.alumno_id == alumno_id).order_by(AlumnoHistorial.anio).all()

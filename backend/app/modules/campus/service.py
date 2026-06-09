import os
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from .models import Tarea, Entrega, Calificacion, MaterialEstudio, DocumentoAlumno, DocumentoCompartido, CompartidoPermiso
from app.modules.academico.materias.models import Materia
from app.modules.academico.alumnos.models import Alumno
from app.modules.academico.archivos.models import Archivo
from app.core.config import FILES_PATH


# ================= TAREAS =================

def crear_tarea(db: Session, data, profesor_id: int):
    tarea = Tarea(
        materia_id=data.materia_id,
        profesor_id=profesor_id,
        titulo=data.titulo,
        descripcion=data.descripcion,
        fecha_limite=data.fecha_limite
    )
    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea


def listar_tareas(db: Session, materia_id: int = None):
    query = db.query(Tarea)
    if materia_id:
        query = query.filter(Tarea.materia_id == materia_id)
    return query.order_by(desc(Tarea.created_at)).all()


def obtener_tarea(db: Session, tarea_id: int):
    return db.query(Tarea).filter(Tarea.id == tarea_id).first()


def actualizar_tarea(db: Session, tarea_id: int, data):
    tarea = obtener_tarea(db, tarea_id)
    if not tarea:
        return None
    if data.titulo is not None:
        tarea.titulo = data.titulo
    if data.descripcion is not None:
        tarea.descripcion = data.descripcion
    if data.fecha_limite is not None:
        tarea.fecha_limite = data.fecha_limite
    if data.materia_id is not None:
        tarea.materia_id = data.materia_id
    db.commit()
    db.refresh(tarea)
    return tarea


def eliminar_tarea(db: Session, tarea_id: int):
    tarea = obtener_tarea(db, tarea_id)
    if not tarea:
        return None
    db.delete(tarea)
    db.commit()
    return tarea


# ================= ENTREGAS =================

def realizar_entrega(db: Session, tarea_id: int, alumno_id: int, archivo_id: int, comentario: str = None):
    existe = db.query(Entrega).filter(
        Entrega.tarea_id == tarea_id,
        Entrega.alumno_id == alumno_id
    ).first()
    if existe:
        raise ValueError("Ya realizaste una entrega para esta tarea")

    entrega = Entrega(
        tarea_id=tarea_id,
        alumno_id=alumno_id,
        archivo_id=archivo_id,
        comentario=comentario
    )
    db.add(entrega)
    db.commit()
    db.refresh(entrega)
    return entrega


def listar_entregas_por_tarea(db: Session, tarea_id: int):
    return db.query(Entrega).filter(Entrega.tarea_id == tarea_id).order_by(desc(Entrega.fecha_entrega)).all()


def listar_mis_entregas(db: Session, alumno_id: int):
    return db.query(Entrega).filter(Entrega.alumno_id == alumno_id).order_by(desc(Entrega.fecha_entrega)).all()


def obtener_entrega(db: Session, entrega_id: int):
    return db.query(Entrega).filter(Entrega.id == entrega_id).first()


# ================= CALIFICACIONES =================

def calificar_entrega(db: Session, entrega_id: int, profesor_id: int, data):
    calif = db.query(Calificacion).filter(Calificacion.entrega_id == entrega_id).first()
    if calif:
        calif.nota = data.nota
        calif.feedback = data.feedback
        calif.fecha_calificacion = datetime.utcnow()
    else:
        calif = Calificacion(
            entrega_id=entrega_id,
            profesor_id=profesor_id,
            nota=data.nota,
            feedback=data.feedback
        )
        db.add(calif)

    entrega = db.query(Entrega).filter(Entrega.id == entrega_id).first()
    if entrega:
        entrega.calificado = True

    db.commit()
    db.refresh(calif)
    return calif


# ================= MATERIALES =================

def crear_material(db: Session, data, profesor_id: int, archivo_id: int = None):
    material = MaterialEstudio(
        materia_id=data.materia_id,
        profesor_id=profesor_id,
        titulo=data.titulo,
        descripcion=data.descripcion,
        archivo_id=archivo_id
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


def listar_materiales(db: Session, materia_id: int = None):
    query = db.query(MaterialEstudio)
    if materia_id:
        query = query.filter(MaterialEstudio.materia_id == materia_id)
    return query.order_by(desc(MaterialEstudio.created_at)).all()


def eliminar_material(db: Session, material_id: int):
    material = db.query(MaterialEstudio).filter(MaterialEstudio.id == material_id).first()
    if not material:
        return None
    db.delete(material)
    db.commit()
    return material


# ================= DOCUMENTOS DEL ALUMNO =================

def crear_carpeta(db: Session, alumno_id: int, nombre: str, padre_id: int = None):
    if padre_id:
        padre = db.query(DocumentoAlumno).filter(DocumentoAlumno.id == padre_id, DocumentoAlumno.alumno_id == alumno_id, DocumentoAlumno.es_carpeta == True).first()
        if not padre:
            raise ValueError("Carpeta padre no encontrada")

    existe = db.query(DocumentoAlumno).filter(
        DocumentoAlumno.alumno_id == alumno_id,
        DocumentoAlumno.nombre == nombre,
        DocumentoAlumno.es_carpeta == True,
        DocumentoAlumno.carpeta_padre_id == padre_id
    ).first()
    if existe:
        raise ValueError("Ya existe una carpeta con ese nombre aquí")

    doc = DocumentoAlumno(alumno_id=alumno_id, nombre=nombre, es_carpeta=True, carpeta_padre_id=padre_id)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def subir_documento(db: Session, alumno_id: int, nombre: str, archivo_id: int, padre_id: int = None):
    if padre_id:
        padre = db.query(DocumentoAlumno).filter(DocumentoAlumno.id == padre_id, DocumentoAlumno.alumno_id == alumno_id, DocumentoAlumno.es_carpeta == True).first()
        if not padre:
            raise ValueError("Carpeta padre no encontrada")

    doc = DocumentoAlumno(
        alumno_id=alumno_id, nombre=nombre, es_carpeta=False,
        carpeta_padre_id=padre_id, archivo_id=archivo_id
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def listar_documentos(db: Session, alumno_id: int, carpeta_id: int = None):
    query = db.query(DocumentoAlumno).filter(
        DocumentoAlumno.alumno_id == alumno_id,
        DocumentoAlumno.carpeta_padre_id == carpeta_id
    )
    return query.order_by(desc(DocumentoAlumno.es_carpeta), DocumentoAlumno.nombre).all()


def obtener_documento(db: Session, doc_id: int, alumno_id: int):
    return db.query(DocumentoAlumno).filter(DocumentoAlumno.id == doc_id, DocumentoAlumno.alumno_id == alumno_id).first()


def eliminar_documento(db: Session, doc_id: int, alumno_id: int):
    doc = obtener_documento(db, doc_id, alumno_id)
    if not doc:
        return None
    if doc.es_carpeta:
        hijos = db.query(DocumentoAlumno).filter(DocumentoAlumno.carpeta_padre_id == doc_id).count()
        if hijos > 0:
            raise ValueError("La carpeta no está vacía")
    db.delete(doc)
    db.commit()
    return doc


def obtener_ruta(db: Session, carpeta_id: int, alumno_id: int):
    ruta = []
    actual = db.query(DocumentoAlumno).filter(DocumentoAlumno.id == carpeta_id, DocumentoAlumno.alumno_id == alumno_id).first()
    while actual:
        ruta.insert(0, {"id": actual.id, "nombre": actual.nombre})
        if actual.carpeta_padre_id:
            actual = db.query(DocumentoAlumno).filter(DocumentoAlumno.id == actual.carpeta_padre_id).first()
        else:
            actual = None
    return ruta


# ================= DOCUMENTOS COMPARTIDOS =================

def crear_carpeta_compartida(db: Session, creador_id: int, nombre: str, padre_id: int = None, permisos: list = None):
    if padre_id:
        padre = db.query(DocumentoCompartido).filter(DocumentoCompartido.id == padre_id, DocumentoCompartido.es_carpeta == True).first()
        if not padre:
            raise ValueError("Carpeta padre no encontrada")

    existe = db.query(DocumentoCompartido).filter(
        DocumentoCompartido.nombre == nombre,
        DocumentoCompartido.es_carpeta == True,
        DocumentoCompartido.carpeta_padre_id == padre_id
    ).first()
    if existe:
        raise ValueError("Ya existe una carpeta con ese nombre aquí")

    doc = DocumentoCompartido(creador_id=creador_id, nombre=nombre, es_carpeta=True, carpeta_padre_id=padre_id)
    db.add(doc)
    db.flush()

    if permisos:
        for p in permisos:
            perm = CompartidoPermiso(carpeta_id=doc.id, tipo=p["tipo"], destino_id=p["destino_id"])
            db.add(perm)

    db.commit()
    db.refresh(doc)
    return doc


def subir_documento_compartido(db: Session, creador_id: int, nombre: str, archivo_id: int, padre_id: int = None):
    if padre_id:
        padre = db.query(DocumentoCompartido).filter(DocumentoCompartido.id == padre_id, DocumentoCompartido.es_carpeta == True).first()
        if not padre:
            raise ValueError("Carpeta padre no encontrada")

    doc = DocumentoCompartido(
        creador_id=creador_id, nombre=nombre, es_carpeta=False,
        carpeta_padre_id=padre_id, archivo_id=archivo_id
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def _tiene_acceso(db: Session, carpeta: DocumentoCompartido, user_id: int, role_id: int) -> bool:
    if carpeta.creador_id == user_id:
        return True
    perms = db.query(CompartidoPermiso).filter(CompartidoPermiso.carpeta_id == carpeta.id).all()
    if not perms:
        return True
    for p in perms:
        if p.tipo == "user" and p.destino_id == user_id:
            return True
        if p.tipo == "role" and p.destino_id == role_id:
            return True
    return False


def listar_documentos_compartidos(db: Session, carpeta_id: int = None, user_id: int = None, role_id: int = None):
    if carpeta_id:
        carpeta = db.query(DocumentoCompartido).filter(DocumentoCompartido.id == carpeta_id).first()
        if not carpeta:
            raise ValueError("Carpeta no encontrada")
        query = db.query(DocumentoCompartido).filter(
            DocumentoCompartido.carpeta_padre_id == carpeta_id
        )
        return query.order_by(desc(DocumentoCompartido.es_carpeta), DocumentoCompartido.nombre).all()

    if user_id is not None and role_id is not None:
        carpetas = db.query(DocumentoCompartido).filter(DocumentoCompartido.carpeta_padre_id == None).all()
        accesibles = [c for c in carpetas if _tiene_acceso(db, c, user_id, role_id)]
        accesibles.sort(key=lambda x: (not x.es_carpeta, x.nombre.lower()))
        return accesibles

    return []


def obtener_ruta_compartida(db: Session, carpeta_id: int):
    ruta = []
    actual = db.query(DocumentoCompartido).filter(DocumentoCompartido.id == carpeta_id).first()
    while actual:
        ruta.insert(0, {"id": actual.id, "nombre": actual.nombre})
        if actual.carpeta_padre_id:
            actual = db.query(DocumentoCompartido).filter(DocumentoCompartido.id == actual.carpeta_padre_id).first()
        else:
            actual = None
    return ruta


def eliminar_documento_compartido(db: Session, doc_id: int):
    doc = db.query(DocumentoCompartido).filter(DocumentoCompartido.id == doc_id).first()
    if not doc:
        return None
    if doc.es_carpeta:
        hijos = db.query(DocumentoCompartido).filter(DocumentoCompartido.carpeta_padre_id == doc_id).count()
        if hijos > 0:
            raise ValueError("La carpeta no está vacía")
    db.delete(doc)
    db.commit()
    return doc

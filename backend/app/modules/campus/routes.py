from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user, require_permission
from app.modules.campus import service, schemas
from app.modules.campus.models import DocumentoCompartido
from app.modules.academico.materias.models import Materia
from app.modules.academico.alumnos.models import Alumno
from app.modules.academico.archivos.service import guardar_archivo
from app.modules.academico.archivos.models import Archivo
from app.modules.academico.alumnos.service import obtener_por_dni
from app.modules.users.users.models import User

router = APIRouter(prefix="/campus", tags=["Campus Virtual"])


# ================= TAREAS =================

@router.post("/tareas/", response_model=schemas.TareaOut)
def crear_tarea(data: schemas.TareaCreate, db: Session = Depends(get_db), user=Depends(get_current_user), _=Depends(require_permission("tareas.create"))):
    tarea = service.crear_tarea(db, data, user["id"])
    materia = db.query(Materia).filter(Materia.id == tarea.materia_id).first()
    tarea.materia_nombre = materia.nombre if materia else None
    return tarea


@router.get("/tareas/", response_model=list[schemas.TareaOut])
def listar_tareas(materia_id: Optional[int] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    tareas = service.listar_tareas(db, materia_id)
    for t in tareas:
        materia = db.query(Materia).filter(Materia.id == t.materia_id).first()
        t.materia_nombre = materia.nombre if materia else None
    return tareas


@router.get("/tareas/{tarea_id}", response_model=schemas.TareaOut)
def obtener_tarea(tarea_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    tarea = service.obtener_tarea(db, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    materia = db.query(Materia).filter(Materia.id == tarea.materia_id).first()
    tarea.materia_nombre = materia.nombre if materia else None
    return tarea


@router.put("/tareas/{tarea_id}", response_model=schemas.TareaOut)
def actualizar_tarea(tarea_id: int, data: schemas.TareaCreate, db: Session = Depends(get_db), user=Depends(get_current_user), _=Depends(require_permission("tareas.edit"))):
    tarea = service.actualizar_tarea(db, tarea_id, data)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    materia = db.query(Materia).filter(Materia.id == tarea.materia_id).first()
    tarea.materia_nombre = materia.nombre if materia else None
    return tarea


@router.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db), user=Depends(get_current_user), _=Depends(require_permission("tareas.delete"))):
    tarea = service.eliminar_tarea(db, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"message": "Tarea eliminada correctamente"}


# ================= ENTREGAS =================

@router.post("/tareas/{tarea_id}/entregar")
def entregar_tarea(
    tarea_id: int,
    file: UploadFile = File(...),
    comentario: str = Form(""),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    tarea = service.obtener_tarea(db, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    alumno = db.query(Alumno).filter(Alumno.user_id == user["id"]).first()
    if not alumno:
        raise HTTPException(status_code=400, detail="No tienes un perfil de alumno asociado")

    try:
        archivo = guardar_archivo(db, alumno, file)
        entrega = service.realizar_entrega(db, tarea_id, alumno.id, archivo.id, comentario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Trabajo entregado correctamente", "entrega_id": entrega.id}


@router.get("/mis-entregas", response_model=list[schemas.EntregaOut])
def mis_entregas(db: Session = Depends(get_db), user=Depends(get_current_user)):
    alumno = db.query(Alumno).filter(Alumno.user_id == user["id"]).first()
    if not alumno:
        raise HTTPException(status_code=400, detail="No tienes un perfil de alumno asociado")

    entregas = service.listar_mis_entregas(db, alumno.id)
    for e in entregas:
        e.alumno_nombre = f"{alumno.nombre} {alumno.apellido}"
        if e.tarea:
            e.tarea_titulo = e.tarea.titulo
            materia = db.query(Materia).filter(Materia.id == e.tarea.materia_id).first()
            e.materia_nombre = materia.nombre if materia else None
        if e.calificacion:
            e.nota = e.calificacion.nota
            e.feedback = e.calificacion.feedback
    return entregas


@router.get("/tareas/{tarea_id}/entregas", response_model=list[schemas.EntregaOut])
def entregas_por_tarea(tarea_id: int, db: Session = Depends(get_db), user=Depends(get_current_user), _=Depends(require_permission("entregas.ver_todas"))):
    tarea = service.obtener_tarea(db, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    entregas = service.listar_entregas_por_tarea(db, tarea_id)
    for e in entregas:
        if e.alumno:
            e.alumno_nombre = f"{e.alumno.nombre} {e.alumno.apellido}"
        if e.tarea:
            e.tarea_titulo = e.tarea.titulo
        if e.calificacion:
            e.nota = e.calificacion.nota
            e.feedback = e.calificacion.feedback
    return entregas


# ================= CALIFICACIONES =================

@router.post("/entregas/{entrega_id}/calificar", response_model=schemas.CalificacionOut)
def calificar_entrega(entrega_id: int, data: schemas.CalificacionCreate, db: Session = Depends(get_db), user=Depends(get_current_user), _=Depends(require_permission("entregas.calificar"))):
    entrega = service.obtener_entrega(db, entrega_id)
    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    return service.calificar_entrega(db, entrega_id, user["id"], data)


# ================= MATERIALES =================

@router.post("/materiales/subir")
def subir_material(
    materia_id: int = Form(...),
    titulo: str = Form(...),
    descripcion: str = Form(""),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    _=Depends(require_permission("materiales.create"))
):
    archivo_id = None
    if file and file.filename:
        alumno_dummy = db.query(Alumno).first()
        if not alumno_dummy:
            alumno_dummy = Alumno(dni="00000000", nombre="Sistema", apellido="Campus")
            db.add(alumno_dummy)
            db.commit()
            db.refresh(alumno_dummy)
        archivo = guardar_archivo(db, alumno_dummy, file)
        archivo_id = archivo.id

    data = schemas.MaterialCreate(materia_id=materia_id, titulo=titulo, descripcion=descripcion)
    material = service.crear_material(db, data, user["id"], archivo_id)
    return {"message": "Material subido correctamente", "material_id": material.id}


@router.get("/materiales/", response_model=list[schemas.MaterialOut])
def listar_materiales(materia_id: Optional[int] = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    materiales = service.listar_materiales(db, materia_id)
    for m in materiales:
        materia = db.query(Materia).filter(Materia.id == m.materia_id).first()
        m.materia_nombre = materia.nombre if materia else None
    return materiales


@router.delete("/materiales/{material_id}")
def eliminar_material(material_id: int, db: Session = Depends(get_db), user=Depends(get_current_user), _=Depends(require_permission("materiales.delete"))):
    material = service.eliminar_material(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return {"message": "Material eliminado correctamente"}


# ================= DOCUMENTOS DEL ALUMNO =================

@router.get("/misdocumentos/")
def listar_documentos(carpeta_id: int = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    alumno = db.query(Alumno).filter(Alumno.user_id == user["id"]).first()
    if not alumno:
        raise HTTPException(status_code=400, detail="No tienes un perfil de alumno asociado")
    docs = service.listar_documentos(db, alumno.id, carpeta_id)
    ruta = service.obtener_ruta(db, carpeta_id, alumno.id) if carpeta_id else []
    resultados = []
    for d in docs:
        item = {"id": d.id, "nombre": d.nombre, "es_carpeta": d.es_carpeta, "created_at": d.created_at.isoformat() if d.created_at else None}
        if not d.es_carpeta:
            item["archivo_id"] = d.archivo_id
        resultados.append(item)
    return {"contenido": resultados, "ruta": ruta}


@router.post("/misdocumentos/carpeta")
def crear_carpeta(nombre: str, carpeta_padre_id: int = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    alumno = db.query(Alumno).filter(Alumno.user_id == user["id"]).first()
    if not alumno:
        raise HTTPException(status_code=400, detail="No tienes un perfil de alumno asociado")
    try:
        doc = service.crear_carpeta(db, alumno.id, nombre, carpeta_padre_id)
        return {"message": "Carpeta creada", "id": doc.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/misdocumentos/subir")
def subir_documento(
    file: UploadFile = File(...),
    carpeta_padre_id: int = Form(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    alumno = db.query(Alumno).filter(Alumno.user_id == user["id"]).first()
    if not alumno:
        raise HTTPException(status_code=400, detail="No tienes un perfil de alumno asociado")

    archivo = guardar_archivo(db, alumno, file)

    try:
        doc = service.subir_documento(db, alumno.id, archivo.nombre_archivo, archivo.id, carpeta_padre_id)
        return {"message": "Archivo subido", "id": doc.id, "archivo_id": archivo.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/misdocumentos/{doc_id}")
def eliminar_documento(doc_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    alumno = db.query(Alumno).filter(Alumno.user_id == user["id"]).first()
    if not alumno:
        raise HTTPException(status_code=400, detail="No tienes un perfil de alumno asociado")
    try:
        doc = service.eliminar_documento(db, doc_id, alumno.id)
        if not doc:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return {"message": "Documento eliminado"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ================= DOCUMENTOS COMPARTIDOS =================

@router.get("/compartidos/")
def listar_compartidos(carpeta_id: int = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        docs = service.listar_documentos_compartidos(db, carpeta_id, user["id"], user["role"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    ruta = service.obtener_ruta_compartida(db, carpeta_id) if carpeta_id else []
    resultados = []
    for d in docs:
        item = {"id": d.id, "nombre": d.nombre, "es_carpeta": d.es_carpeta, "created_at": d.created_at.isoformat() if d.created_at else None}
        if not d.es_carpeta:
            item["archivo_id"] = d.archivo_id
        resultados.append(item)
    return {"contenido": resultados, "ruta": ruta}


@router.post("/compartidos/carpeta")
def crear_carpeta_compartida(
    nombre: str,
    carpeta_padre_id: int = None,
    permisos: str = "[]",
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    _=Depends(require_permission("compartidos.create"))
):
    import json
    try:
        lista_permisos = json.loads(permisos)
    except json.JSONDecodeError:
        lista_permisos = []
    try:
        doc = service.crear_carpeta_compartida(db, user["id"], nombre, carpeta_padre_id, lista_permisos)
        return {"message": "Carpeta compartida creada", "id": doc.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compartidos/subir")
def subir_documento_compartido(
    file: UploadFile = File(...),
    carpeta_padre_id: int = Form(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    _=Depends(require_permission("compartidos.create"))
):
    alumno_dummy = db.query(Alumno).first()
    if not alumno_dummy:
        alumno_dummy = Alumno(dni="00000000", nombre="Sistema", apellido="Compartidos")
        db.add(alumno_dummy)
        db.commit()
        db.refresh(alumno_dummy)
    archivo = guardar_archivo(db, alumno_dummy, file)

    try:
        doc = service.subir_documento_compartido(db, user["id"], archivo.nombre_archivo, archivo.id, carpeta_padre_id)
        return {"message": "Archivo compartido subido", "id": doc.id, "archivo_id": archivo.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/compartidos/{doc_id}")
def eliminar_documento_compartido(doc_id: int, db: Session = Depends(get_db), user=Depends(get_current_user), _=Depends(require_permission("compartidos.delete"))):
    try:
        doc = service.eliminar_documento_compartido(db, doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return {"message": "Documento compartido eliminado"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

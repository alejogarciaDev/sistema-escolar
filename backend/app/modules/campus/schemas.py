from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TareaCreate(BaseModel):
    materia_id: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_limite: Optional[datetime] = None


class TareaOut(BaseModel):
    id: int
    materia_id: int
    profesor_id: int
    titulo: str
    descripcion: Optional[str]
    fecha_limite: Optional[datetime]
    activa: bool
    created_at: datetime
    materia_nombre: Optional[str] = None

    class Config:
        from_attributes = True


class EntregaCreate(BaseModel):
    tarea_id: int
    comentario: Optional[str] = None


class EntregaOut(BaseModel):
    id: int
    tarea_id: int
    alumno_id: int
    archivo_id: Optional[int]
    comentario: Optional[str]
    fecha_entrega: datetime
    calificado: bool
    alumno_nombre: Optional[str] = None
    tarea_titulo: Optional[str] = None
    materia_nombre: Optional[str] = None
    nota: Optional[float] = None
    feedback: Optional[str] = None

    class Config:
        from_attributes = True


class CalificacionCreate(BaseModel):
    nota: float
    feedback: Optional[str] = None


class CalificacionOut(BaseModel):
    id: int
    entrega_id: int
    profesor_id: int
    nota: float
    feedback: Optional[str]
    fecha_calificacion: datetime

    class Config:
        from_attributes = True


class MaterialCreate(BaseModel):
    materia_id: int
    titulo: str
    descripcion: Optional[str] = None


class MaterialOut(BaseModel):
    id: int
    materia_id: int
    profesor_id: int
    titulo: str
    descripcion: Optional[str]
    archivo_id: Optional[int]
    created_at: datetime
    materia_nombre: Optional[str] = None

    class Config:
        from_attributes = True

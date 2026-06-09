from pydantic import BaseModel
from typing import Optional


class AlumnoCreate(BaseModel):
    dni: str
    nombre: str
    apellido: str


class AlumnoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    folio: Optional[str] = None
    legajo: Optional[str] = None


class HistorialCreate(BaseModel):
    anio: str
    curso: str
    repitio: bool = False
    observaciones: Optional[str] = None


class HistorialOut(BaseModel):
    id: int
    anio: str
    curso: str
    repitio: bool
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True


class AlumnoOut(BaseModel):
    id: int
    dni: str
    nombre: str
    apellido: str
    folio: Optional[str] = None
    legajo: Optional[str] = None
    historial: list[HistorialOut] = []

    class Config:
        from_attributes = True


class AlumnoSimple(BaseModel):
    id: int
    dni: str
    nombre: str
    apellido: str
    folio: Optional[str] = None
    legajo: Optional[str] = None

    class Config:
        from_attributes = True

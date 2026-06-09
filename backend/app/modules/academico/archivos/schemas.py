from pydantic import BaseModel
from datetime import datetime

class ArchivoOut(BaseModel):
    id: int
    nombre_archivo: str
    ruta_archivo: str
    tipo: str
    fecha_subida: datetime

    class Config:
        from_attributes = True
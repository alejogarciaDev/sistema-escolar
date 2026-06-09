from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Archivo(Base):
    __tablename__ = "archivos"

    id = Column(Integer, primary_key=True, index=True)

    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=True)

    nombre_archivo = Column(String, nullable=False)
    ruta_archivo = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # pdf, jpg, etc

    fecha_subida = Column(DateTime, default=datetime.utcnow)
    
    alumno = relationship("Alumno", backref="archivos")
    materia = relationship("Materia", backref="archivos")
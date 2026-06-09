from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Alumno(Base):
    __tablename__ = "alumnos"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String, unique=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    folio = Column(String, nullable=True)
    legajo = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", backref="alumno_profile")

    historial = relationship("AlumnoHistorial", back_populates="alumno", cascade="all, delete-orphan", order_by="AlumnoHistorial.anio")


class AlumnoHistorial(Base):
    __tablename__ = "alumno_historial"

    id = Column(Integer, primary_key=True, index=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    anio = Column(String, nullable=False)
    curso = Column(String, nullable=False)
    repitio = Column(Boolean, default=False)
    observaciones = Column(Text, nullable=True)

    alumno = relationship("Alumno", back_populates="historial")

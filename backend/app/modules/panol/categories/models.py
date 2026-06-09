from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    barcode = Column(String, unique=True, index=True, nullable=True)
    stock = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
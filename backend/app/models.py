from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


# 👤 USUARIO
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")

    loans = relationship("Loan", back_populates="user")


# 🎭 ROL
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


# 📁 CATEGORIA (TIPO DE HERRAMIENTA)
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    barcode = Column(String, unique=True, index=True, nullable=True)
    stock = Column(Integer, default=0)
    activo = Column(Boolean, default=True)




# 📦 PRÉSTAMO
class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    panolero_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    quantity = Column(Integer, default=1)

    description_loan = Column(String, nullable=True)
    description_return = Column(String, nullable=True)

    borrowed_at = Column(DateTime, default=datetime.utcnow)
    returned_at = Column(DateTime, nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="loans")
    panolero = relationship("User", foreign_keys=[panolero_id])
    category = relationship("Category")

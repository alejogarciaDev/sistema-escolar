from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)   # 👈 nombre real (visible)
    email = Column(String, unique=True, index=True, nullable=False)  # 👈 login

    password = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"))

    # 🔗 relación con rol
    role = relationship("Role")
    # relación con préstamos (si usás Loan)
    loans = relationship("Loan", foreign_keys="[Loan.user_id]", back_populates="user")

    # 🔗 permisos extra (tipo Discord)
    permissions = relationship(
        "Permission",
        secondary="user_permissions",
        back_populates="users"
    )
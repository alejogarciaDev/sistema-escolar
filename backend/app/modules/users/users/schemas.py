from pydantic import BaseModel, EmailStr
from typing import List


# =========================
# CREAR USUARIO
# =========================
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: int


# =========================
# RESPUESTA
# =========================
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int

    class Config:
        from_attributes = True


# opcional
class UserWithPermissions(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    permissions: List[str] = []

    class Config:
        from_attributes = True
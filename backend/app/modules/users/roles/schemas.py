from pydantic import BaseModel


# =========================
# CREAR ROL
# =========================
class RoleCreate(BaseModel):
    name: str


# =========================
# RESPUESTA
# =========================
class RoleOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
from pydantic import BaseModel
from typing import List


# 🔹 ITEM INDIVIDUAL
class OrderItemCreate(BaseModel):
    category_id: int
    quantity: int


# 🔹 CREACIÓN DE PEDIDO
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


# 🔹 RESPUESTA
class OrderItemOut(BaseModel):
    category_id: int
    quantity: int
    category_name: str | None = None

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    user_id: int
    profesor: str | None = None
    status: str
    items: List[OrderItemOut]

    class Config:
        from_attributes = True

class OrderDeliver(BaseModel):
    description_loan: str | None = None

class OrderManualCreate(BaseModel):
    user_id: int
    category_id: int
    quantity: int
    description_loan: str | None = None
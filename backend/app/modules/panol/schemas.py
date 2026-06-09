# app/modules/panol/schemas.py

from pydantic import BaseModel

class DeliverOrder(BaseModel):
    barcodes: list

class OrderCreate(BaseModel):
    items: list

class ToolCreate(BaseModel):
    category_id: int

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role_id: int

class CategoryCreate(BaseModel):
    name: str

class RoleCreate(BaseModel):
    name: str
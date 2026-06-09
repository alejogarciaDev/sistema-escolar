from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    barcode: str | None = None
    stock: int = 0

class CategoryOut(BaseModel):
    id: int
    name: str
    barcode: str | None = None
    stock: int
    activo: bool

    class Config:
        from_attributes = True
class AddStock(BaseModel):
    quantity: int

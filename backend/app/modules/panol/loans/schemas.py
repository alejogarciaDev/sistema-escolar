from pydantic import BaseModel

class ReturnByCategory(BaseModel):
    category_barcode: str
    user_id: int
    quantity: int
    description_return: str | None = None
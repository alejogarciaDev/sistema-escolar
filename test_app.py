from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class AddStock(BaseModel):
    quantity: int

@app.post("/categories/{category_id}/add-stock")
def add_stock(category_id: int, data: AddStock):
    return {"status": "ok", "cat": category_id, "qty": data.quantity}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8002)

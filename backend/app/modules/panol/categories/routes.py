from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from . import schemas, service

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=schemas.CategoryOut)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return service.create_category(db, category)

@router.get("/", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return service.get_categories(db)

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return service.delete_category(db, category_id)

@router.get("/summary")
def category_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    from app.modules.panol.categories.models import Category
    categories = db.query(Category).all()
    return [{"category_id": cat.id, "category_name": cat.name, "available": cat.stock, "total": cat.stock} for cat in categories]

@router.post("/add-stock/{category_id}")
def add_stock(category_id: int, data: schemas.AddStock, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from app.modules.panol.categories.models import Category
    from fastapi import HTTPException
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=400, detail="Categoria no encontrada en DB (ID: " + str(category_id) + ")")
    if data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Cantidad invalida")
    cat.stock += data.quantity
    db.commit()
    return {"message": "Stock actualizado", "new_stock": cat.stock}

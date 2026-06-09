from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models

import uuid

# =========================
# CREAR CATEGORÍA
# =========================
def create_category(db: Session, data):

    existing = db.query(models.Category).filter(models.Category.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
        
    if data.barcode:
        existing_barcode = db.query(models.Category).filter(models.Category.barcode == data.barcode).first()
        if existing_barcode:
            raise HTTPException(status_code=400, detail="El código de barras ya está en uso")
    else:
        # Generar código de barras automático si no se provee (ej: CAT-A3F9B)
        data.barcode = f"CAT-{uuid.uuid4().hex[:6].upper()}"

    category = models.Category(
        name=data.name,
        barcode=data.barcode,
        stock=data.stock,
        activo=True
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


# =========================
# LISTAR CATEGORÍAS
# =========================
def get_categories(db: Session):
    return db.query(models.Category).all()


# =========================
# ELIMINAR CATEGORÍA
# =========================
def delete_category(db: Session, category_id: int):

    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db.delete(category)
    db.commit()

    return {"message": "Categoría eliminada"}
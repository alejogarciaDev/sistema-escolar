from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Order
from .items.models import OrderItem
from app.modules.panol.loans.service import create_loan
from app.modules.panol.categories.models import Category

def create_order(db: Session, user_id: int, items):
    order = Order(user_id=user_id, status="pendiente")
    db.add(order)
    db.flush()

    for item in items:
        # Validar stock
        cat = db.query(Category).filter(Category.id == item["category_id"]).first()
        if not cat:
            raise HTTPException(status_code=400, detail="Categoría no encontrada")
        if cat.stock < item["quantity"]:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {cat.name}")

        order_item = OrderItem(
            order_id=order.id,
            category_id=item["category_id"],
            quantity=item["quantity"]
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)
    return order

def prepare_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if order.status != "pendiente":
        raise HTTPException(status_code=400, detail="Solo pedidos pendientes pueden prepararse")
    
    order.status = "preparado"
    db.commit()
    return order

def deliver_order(db: Session, order_id: int, panolero_id: int, description_loan: str | None = None):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if order.status not in ["pendiente", "preparado"]:
        raise HTTPException(status_code=400, detail="El pedido no se puede entregar")

    created_loans = []
    
    for item in order.items:
        # Descontar stock
        cat = db.query(Category).filter(Category.id == item.category_id).first()
        if not cat or cat.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente en la categoría {item.category_id}")
            
        cat.stock -= item.quantity
        
        loan = create_loan(
            db=db, 
            user_id=order.user_id, 
            panolero_id=panolero_id,
            category_id=item.category_id,
            quantity=item.quantity,
            order_id=order.id,
            description_loan=description_loan
        )
        created_loans.append(loan)

    order.status = "entregado"
    db.commit()

    return {"message": "Pedido entregado", "loans": len(created_loans)}
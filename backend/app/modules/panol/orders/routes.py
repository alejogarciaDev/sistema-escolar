from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.modules.users.users.models import User
from . import service, schemas
from .models import Order

router = APIRouter(prefix="/orders", tags=["Orders"])


# =========================
# CREAR PEDIDO (PROFESOR)
# =========================
@router.post("/", response_model=schemas.OrderOut)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return service.create_order(
        db,
        user["id"],   # 🔥 FIX CLAVE
        [item.dict() for item in order.items]
    )


# =========================
# VER PEDIDOS PENDIENTES Y PREPARADOS (PAÑOL)
# =========================
@router.get("/pending", response_model=list[schemas.OrderOut])
def get_pending_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return (
        db.query(Order)
        .join(User, Order.user_id == User.id)
        .filter(Order.status.in_(["pendiente", "preparado"]))
        .all()
    )

# =========================
# VER MIS PEDIDOS (PROFESOR)
# =========================
@router.get("/my", response_model=list[schemas.OrderOut])
def get_my_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Order).filter(Order.user_id == user["id"]).all()

# =========================
# PREPARAR PEDIDO
# =========================
@router.put("/{order_id}/prepare", response_model=schemas.OrderOut)
def prepare_order_route(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return service.prepare_order(db, order_id)

# =========================
# ENTREGAR PEDIDO
# =========================
@router.put("/{order_id}/deliver")
def deliver_order_route(
    order_id: int,
    data: schemas.OrderDeliver,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return service.deliver_order(db, order_id, user["id"], data.description_loan)

# =========================
# PEDIDO MANUAL DIRECTO
# =========================
@router.post("/manual")
def create_manual_order(
    data: schemas.OrderManualCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Crear y entregar de una
    order = service.create_order(
        db,
        data.user_id,
        [{"category_id": data.category_id, "quantity": data.quantity}]
    )
    return service.deliver_order(db, order.id, user["id"], data.description_loan)
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from .models import Loan
from app.modules.users.users.models import User
from app.modules.panol.categories.models import Category


# =========================
# CREAR PRÉSTAMO (AL ENTREGAR PEDIDO)
# =========================
def create_loan(db: Session, user_id: int, panolero_id: int, category_id: int, quantity: int, order_id: int | None = None, description_loan: str | None = None):
    loan = Loan(
        user_id=user_id,
        panolero_id=panolero_id,
        category_id=category_id,
        quantity=quantity,
        order_id=order_id,
        description_loan=description_loan,
        status="active"
    )

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return loan


# =========================
# DEVOLVER HERRAMIENTA POR CATEGORÍA
# =========================
def return_tools_by_category(db: Session, category_barcode: str, user_id: int, quantity: int, description_return: str | None = None):
    
    category = db.query(Category).filter(Category.barcode == category_barcode).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    loans = (
        db.query(Loan)
        .filter(Loan.category_id == category.id, Loan.user_id == user_id, Loan.returned_at.is_(None))
        .all()
    )

    total_prestado = sum([l.quantity for l in loans])
    if total_prestado < quantity:
        raise HTTPException(status_code=400, detail=f"El profesor solo tiene {total_prestado} herramientas prestadas de esta categoría")

    # Devolver cantidad
    remaining_to_return = quantity
    for loan in loans:
        if remaining_to_return <= 0:
            break
            
        if loan.quantity <= remaining_to_return:
            remaining_to_return -= loan.quantity
            loan.returned_at = datetime.utcnow()
            loan.status = "returned"
            loan.description_return = description_return
        else:
            # Separar el prestamo en dos: uno devuelto y uno activo
            new_loan = Loan(
                user_id=loan.user_id,
                panolero_id=loan.panolero_id,
                category_id=loan.category_id,
                quantity=loan.quantity - remaining_to_return,
                order_id=loan.order_id,
                description_loan=loan.description_loan,
                status="active"
            )
            db.add(new_loan)
            
            loan.quantity = remaining_to_return
            loan.returned_at = datetime.utcnow()
            loan.status = "returned"
            loan.description_return = description_return
            remaining_to_return = 0

    category.stock += quantity
    db.commit()

    return {"message": f"{quantity} herramientas devueltas"}


def get_active_loans(db: Session):
    loans = (
        db.query(Loan)
        .join(User, Loan.user_id == User.id)
        .filter(Loan.returned_at.is_(None))
        .all()
    )

    return [
        {
            "category_name": loan.category.name if loan.category else "Desconocida",
            "quantity": loan.quantity,
            "user": loan.user.name
        }
        for loan in loans
    ]

# =========================
# PRESTAMOS POR PROFESOR
# =========================
def get_loans_grouped_by_professor(db: Session):

    loans = (
        db.query(Loan)
        .join(User, Loan.user_id == User.id)
        .filter(Loan.returned_at.is_(None))
        .all()
    )

    result = {}

    for loan in loans:
        professor_name = loan.user.name

        if professor_name not in result:
            result[professor_name] = []

        result[professor_name].append({
            "category": loan.category.name if loan.category else "Desconocida",
            "barcode": loan.category.barcode if loan.category else None,
            "quantity": loan.quantity
        })

    return [
        {
            "profesor": name,
            "tools": items
        }
        for name, items in result.items()
    ]


# =========================
# HISTORIAL DE PRESTAMOS
# =========================
def get_loans_history(db: Session, date_filter: str | None = None):
    query = (
        db.query(Loan)
        .join(User, Loan.user_id == User.id)
    )

    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            from sqlalchemy import cast, Date
            query = query.filter(cast(Loan.borrowed_at, Date) == filter_date)
        except ValueError:
            pass

    loans = query.order_by(Loan.borrowed_at.desc()).all()

    return [
        {
            "id": loan.id,
            "profesor": loan.user.name or f"Profesor {loan.user_id}",
            "panolero": loan.panolero.name if loan.panolero else "N/A",
            "categoria": loan.category.name if loan.category else "Desconocida",
            "cantidad": loan.quantity,
            "nota_entrega": loan.description_loan,
            "nota_devolucion": loan.description_return,
            "fecha_prestamo": loan.borrowed_at.isoformat() if loan.borrowed_at else None,
            "fecha_devolucion": loan.returned_at.isoformat() if loan.returned_at else None,
            "estado": loan.status
        }
        for loan in loans
    ]
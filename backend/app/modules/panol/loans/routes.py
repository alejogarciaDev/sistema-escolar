from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from . import service, schemas

router = APIRouter(prefix="/loans", tags=["Loans"])


# =========================
# DEVOLVER (NUEVO POR CATEGORÍA)
# =========================
@router.post("/return")
def return_tool(
    data: schemas.ReturnByCategory,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return service.return_tools_by_category(
        db, 
        category_barcode=data.category_barcode, 
        user_id=data.user_id, 
        quantity=data.quantity, 
        description_return=data.description_return
    )


# =========================
# ACTIVOS
# =========================
@router.get("/active")
def get_active_loans(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return service.get_active_loans(db)


# =========================
# AGRUPADOS POR PROFESOR
# =========================
@router.get("/active/by-professor")
def loans_grouped_by_professor(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return service.get_loans_grouped_by_professor(db)


# =========================
# HISTORIAL
# =========================
@router.get("/history")
def get_history(
    date_filter: str = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return service.get_loans_history(db, date_filter)


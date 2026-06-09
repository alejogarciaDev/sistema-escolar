# app/modules/panol/status/utils.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Tool

from app.modules.panol.status.utils import get_tool_status

router = APIRouter()

@router.get("/tools/status/all")
def status_all(db: Session = Depends(get_db)):

    tools = db.query(Tool).all()

    return [
        {
            "barcode": t.barcode,
            "status": get_tool_status(db, t)
        }
        for t in tools
    ]  
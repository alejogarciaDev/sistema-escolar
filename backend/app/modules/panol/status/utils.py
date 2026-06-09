from sqlalchemy.orm import Session
from app.models import Tool, Loan

def get_tool_status(db: Session, tool: Tool):

    if not tool:
        return "unknown"

    if tool.status == "rota":
        return "rota"

    active = db.query(Loan).filter(
        Loan.tool_id == tool.id,
        Loan.returned_at == None
    ).first()

    if active:
        return "prestada"

    return tool.status
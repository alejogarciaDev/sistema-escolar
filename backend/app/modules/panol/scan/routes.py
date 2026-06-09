@app.post("/scan/assign")
def scan_assign(code: str, user=Depends(get_current_user), db: Session = Depends(get_db)):

    tool = db.query(Tool).filter(Tool.barcode == code).first()

    if not tool:
        raise HTTPException(404)

    loan = db.query(Loan).filter(
        Loan.user_id == user.id,
        Loan.tool_id == None,
        Loan.returned_at == None
    ).first()

    if not loan:
        raise HTTPException(400, "sin solicitud")

    loan.tool_id = tool.id
    tool.status = "active"

    db.commit()

    return {"msg": "asignada"}
@app.post("/scan/return")
def scan_return(code: str, db: Session = Depends(get_db)):

    tool = db.query(Tool).filter(Tool.barcode == code).first()

    if not tool:
        raise HTTPException(404)

    loan = db.query(Loan).filter(
        Loan.tool_id == tool.id,
        Loan.returned_at == None
    ).first()

    if not loan:
        raise HTTPException(400)

    loan.returned_at = datetime.utcnow()
    tool.status = "disponible"

    db.commit()

    return {"msg": "devuelta"}

from sqlalchemy.orm import joinedload
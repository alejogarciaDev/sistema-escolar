@app.post("/roles")
def create_role(role: RoleCreate, db: Session = Depends(get_db), admin=Depends(admin_required)):

    if db.query(Role).filter(Role.name == role.name).first():
        raise HTTPException(400, "Existe")

    new_role = Role(name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role


@app.get("/roles")
def get_roles(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Role).all()


@app.delete("/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db), admin=Depends(admin_required)):

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(404)

    if db.query(User).filter(User.role_id == role_id).first():
        raise HTTPException(400, "Tiene usuarios")

    db.delete(role)
    db.commit()

    return {"msg": "eliminado"}


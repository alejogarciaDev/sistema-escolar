from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from .models import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/")
def list_notifications(db: Session = Depends(get_db), user=Depends(get_current_user)):
    notifs = db.query(Notification).filter(
        Notification.user_id == user["id"]
    ).order_by(Notification.created_at.desc()).limit(50).all()
    return [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "type": n.type,
            "read": n.read,
            "created_at": n.created_at.isoformat() if n.created_at else None
        }
        for n in notifs
    ]


@router.get("/unread-count")
def unread_count(db: Session = Depends(get_db), user=Depends(get_current_user)):
    count = db.query(Notification).filter(
        Notification.user_id == user["id"],
        Notification.read == False
    ).count()
    return {"count": count}


@router.put("/{notification_id}/read")
def mark_read(notification_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    notif = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user["id"]
    ).first()
    if notif:
        notif.read = True
        db.commit()
    return {"message": "ok"}


@router.put("/read-all")
def mark_all_read(db: Session = Depends(get_db), user=Depends(get_current_user)):
    db.query(Notification).filter(
        Notification.user_id == user["id"],
        Notification.read == False
    ).update({"read": True})
    db.commit()
    return {"message": "ok"}

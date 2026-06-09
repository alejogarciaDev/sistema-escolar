from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
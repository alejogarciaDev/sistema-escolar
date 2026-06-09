from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    quantity = Column(Integer)

    category = relationship("Category")
    order = relationship("Order", back_populates="items")

    @property
    def category_name(self):
        return self.category.name if self.category else None
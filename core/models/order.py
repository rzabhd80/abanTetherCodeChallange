from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Index, DateTime
from core.models.base import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    currency = Column(String(10), index=True)
    amount = Column(Float)
    status = Column(String(20), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_user_currency', user_id, currency),
    )

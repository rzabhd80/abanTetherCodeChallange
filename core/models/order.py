from datetime import datetime
from enum import Enum as ModelEnum
from sqlalchemy import Column, Integer, String, Float, Index, DateTime, Enum
from core.models.base import Base


class OrderStatusEnum(ModelEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    currency = Column(String(10), index=True)
    amount = Column(Float)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING, index=True)  # Use Enum for status
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_user_currency', user_id, currency),
    )

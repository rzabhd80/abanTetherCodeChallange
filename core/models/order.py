from sqlalchemy import Column, Integer, String, Float, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    currency = Column(String(10), index=True)
    amount = Column(Float)
    status = Column(String(20), index=True)

    __table_args__ = (
        Index('idx_user_currency', user_id, currency),
    )

from sqlalchemy import Column, Integer, String, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from core.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True)
    balance = Column(Float, default=0.0)

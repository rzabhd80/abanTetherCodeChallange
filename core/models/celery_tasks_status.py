from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Index, DateTime
from core.models.base import Base


class TaskStatus(Base):
    __tablename__ = "task_statuses"
    id = Column(Integer, primary_key=True)
    celery_task_id = Column(String(50), unique=True, index=True)
    status = Column(String(20), index=True)
    retries = Column(Integer, default=0)
    last_retry = Column(DateTime)
    result = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

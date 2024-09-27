from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Index, DateTime, Enum
from core.models.base import Base

from enum import Enum as ModelEnum


class TaskStatusEnum(ModelEnum):
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CIRCUIT_OPEN = "CIRCUIT_OPEN"
    RETRYING = "RETRYING"


class TaskStatus(Base):
    __tablename__ = "task_statuses"
    id = Column(Integer, primary_key=True)
    celery_task_id = Column(String(50), unique=True, index=True)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.STARTED, index=True)
    retries = Column(Integer, default=0)
    last_retry = Column(DateTime)
    result = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

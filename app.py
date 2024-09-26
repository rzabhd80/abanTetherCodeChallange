from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.database import DatabaseConfig
from core.mediator.mediator import Mediator
from core.taskQueue.tasks import retry_failed_tasks
from core.models.base import Base
from core.taskQueue.tasks import celery_app

router = FastAPI()
mediator = Mediator()


@router.on_event("startup")
async def startup_event():
    async with DatabaseConfig.get_db().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    #    mediator.register(CreateOrderCommand, CreateOrderHandler)
    celery_app.add_periodic_task(300.0, retry_failed_tasks.s(), name='retry_failed_tasks')

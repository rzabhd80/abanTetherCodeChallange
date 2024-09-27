from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.order.commands.create_order_command import CreateOrderCommand
from api.order.handlers.create_order_handler import CreateOrderHandler
from core.database.database import DatabaseConfig
from core.mediator.mediator import Mediator
from core.taskQueue.tasks import retry_failed_tasks
from core.models.base import Base
from core.taskQueue.tasks import celery_app
from api.order.service import router as order_service

router = FastAPI()
mediator = Mediator()


@router.on_event("startup")
async def startup_event():
    DatabaseConfig.init_database()
    async with DatabaseConfig.get_db().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        create_order_handler = CreateOrderHandler(DatabaseConfig.get_db())
        mediator.register(CreateOrderCommand, create_order_handler)
    celery_app.add_periodic_task(300.0, retry_failed_tasks.s(), name='retry_failed_tasks')


router.include_router(order_service)

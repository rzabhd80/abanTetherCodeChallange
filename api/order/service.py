from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.order.commands.create_order_command import CreateOrderCommand
from api.order.handlers.create_order_handler import CreateOrderHandler
from core.database.database import DatabaseConfig
from core.mediator.mediator import Mediator
from core.taskQueue.tasks import retry_failed_tasks
from core.models.base import Base
from core.taskQueue.tasks import celery_app

router = FastAPI()
mediator = Mediator()


@router.post("/order")
async def create_order(order: CreateOrderCommand, db: AsyncSession = Depends(DatabaseConfig.get_db)):
    try:
        # Check if the amount is valid before proceeding
        if order.amount < 10.0:
            raise HTTPException(status_code=400, detail="Minimum purchase amount is $10")

        handler = CreateOrderHandler(db)
        order_id = await mediator.send(order)
        return {"order_id": order_id, "status": "Order placed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing your order")

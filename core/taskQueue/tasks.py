# tasks.py
import random

from pybreaker import CircuitBreakerError

from core.models.celery_tasks_status import TaskStatus
from core.models.order import Order
from core.taskQueue.celery_queue import configure_celery
from services.task_status_service import TaskStatusService, OrderStatusService
from core.taskQueue.circut_breaker import setup_circuit_breaker
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

celery_app = configure_celery()
breaker = setup_circuit_breaker()


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def buy_from_exchange(self, order_id: int, currency: str, amount: float):
    task_status = None
    session = Session()
    task_status_service = TaskStatusService(session)
    order_status_service = OrderStatusService(session)

    try:
        task_status = task_status_service.create_task_status(celery_task_id=self.request.id)

        result = breaker.call(perform_exchange_buy, currency, amount)
        order_status_service.update_order_status(order_id, "completed")

        task_status_service.update_task_status(task_status, "success", result=str(result))

        return result

    except CircuitBreakerError as e:
        task_status_service.update_task_status(task_status, "circuit_open")
        raise self.retry(exc=e, countdown=300)  # Retry after 5 minutes

    except Exception as e:
        task_status_service.update_task_status(task_status, "failed", retries=task_status.retries + 1)
        raise self.retry(exc=e)

    finally:
        session.close()


def perform_exchange_buy(currency: str, amount: float):
    # Simulate HTTP request to exchange
    random_num = random.randint(0, 1)
    return {"status": "success", "bought": amount, "currency": currency} if random_num == 1 else {"status": "failed",
                                                                                                  "bought": amount,
                                                                                                  "currency": currency}


@celery_app.task
def retry_failed_tasks():
    session = Session()
    try:
        failed_tasks = session.query(TaskStatus).filter(
            TaskStatus.status.in_(["FAILED", "CIRCUIT_OPEN"]),
            TaskStatus.retries < 3,
            TaskStatus.last_retry < datetime.utcnow() - timedelta(minutes=5)
        ).all()

        for task in failed_tasks:
            order = session.query(Order).filter_by(id=task.id).first()
            if order:
                buy_from_exchange.apply_async((order.id, order.currency, order.amount))
                task.retries += 1
                task.last_retry = datetime.utcnow()

        session.commit()
    finally:
        session.close()
# tasks.py
import random

from pybreaker import CircuitBreakerError

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

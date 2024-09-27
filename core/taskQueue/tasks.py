# tasks.py
import random
import uuid

from pybreaker import CircuitBreakerError

from core.models.celery_tasks_status import TaskStatus
from core.models.order import Order
from core.taskQueue.celery_queue import configure_celery
from services.task_status_service import TaskStatusService, OrderStatusService
from core.models.order import OrderStatusEnum
from core.taskQueue.circut_breaker import setup_circuit_breaker
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

celery_app = configure_celery()
breaker = setup_circuit_breaker()


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_accumulated_orders(self):
    session = Session()
    try:
        pending_orders = session.query(Order).filter(Order.status == OrderStatusEnum.PENDING).all()

        orders_by_currency = {}
        for order in pending_orders:
            if order.currency not in orders_by_currency:
                orders_by_currency[order.currency] = []
            orders_by_currency[order.currency].append(order)

        for currency, orders in orders_by_currency.items():
            total_amount = sum(order.amount for order in orders)
            if total_amount >= 10 or len(orders) > 1:
                batch_id = str(uuid.uuid4())
                result = perform_exchange_buy(currency, total_amount)

                # Update orders
                for order in orders:
                    order.status = OrderStatusEnum.COMPLETED if result[
                                                                    'status'] == 'success' else OrderStatusEnum.FAILED
                    order.batch_id = batch_id

                session.commit()

        return {"status": "success", "processed_orders": len(pending_orders)}
    except Exception as e:
        session.rollback()
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

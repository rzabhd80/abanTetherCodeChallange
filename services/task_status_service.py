# services/status_services.py

from core.models.celery_tasks_status import TaskStatus
from core.models.order import Order
from datetime import datetime


class TaskStatusService:
    def __init__(self, session):
        self.session = session

    def create_task_status(self, celery_task_id):
        task_status = TaskStatus(
            celery_task_id=celery_task_id,
            status="STARTED",
            created_at=datetime.utcnow()
        )
        self.session.add(task_status)
        self.session.commit()
        return task_status

    def update_task_status(self, task_status, status, result=None, retries=None, circuit_open=False):
        task_status.status = status
        task_status.result = result if result else task_status.result
        task_status.retries = retries if retries is not None else task_status.retries
        task_status.last_retry = datetime.utcnow()

        if circuit_open:
            task_status.status = "CIRCUIT_OPEN"

        self.session.commit()


class OrderStatusService:
    def __init__(self, session):
        self.session = session

    def update_order_status(self, order_id, status):
        order = self.session.query(Order).get(order_id)
        if order:
            order.status = status
            self.session.commit()
            return order
        return None

from sqlalchemy.ext.asyncio import AsyncSession

from api.order.commands.create_order_command import CreateOrderCommand
from core.cqrs.base_cqrs import Handler
from core.models.order import Order
from core.models.order import OrderStatusEnum
from core.taskQueue.tasks import process_accumulated_orders
from core.models.user import User


class CreateOrderHandler:
    def __init__(self, db: AsyncSession):
        self.db = db

    class CreateOrderHandler(Handler):
        def __init__(self, db: AsyncSession):
            self.db = db

        async def handle(self, command: CreateOrderCommand):
            async with self.db.begin():
                user = await self.db.get(User, command.user_id)
                if not user or user.balance < 4:  # We always deduct $4, regardless of order size
                    raise ValueError("Insufficient balance")

                order = Order(
                    user_id=command.user_id,
                    currency=command.currency,
                    amount=command.amount,
                    status=OrderStatusEnum.PENDING
                )
                self.db.add(order)
                user.balance -= 4
                await self.db.commit()
                await self.db.flush()

            # Trigger the accumulation task
            process_accumulated_orders.delay()

            return order.id

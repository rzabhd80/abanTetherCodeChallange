from sqlalchemy.ext.asyncio import AsyncSession

from api.order.commands.create_order_command import CreateOrderCommand
from core.models.order import Order
from core.models.user import User


class CreateOrderHandler:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def handle(self, command: CreateOrderCommand):
        if command.amount < 10.0:
            raise ValueError("Minimum purchase amount is $10")

        # Check if user exists
        user = await self.db.get(User, command.user_id)
        if not user:
            raise ValueError("User not found")

        new_order = Order(
            user_id=command.user_id,
            currency=command.currency,
            amount=command.amount,
            status="PENDING"
        )
        self.db.add(new_order)
        await self.db.commit()

        return new_order.id

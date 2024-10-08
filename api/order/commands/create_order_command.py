from core.cqrs.base_cqrs import Request


class CreateOrderCommand(Request):
    def __init__(self, user_id: int, amount: float):
        self.user_id = user_id
        self.currency = "ABAN"
        self.amount = amount

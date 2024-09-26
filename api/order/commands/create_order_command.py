class CreateOrderCommand:
    def __init__(self, user_id: int, currency: str, amount: float):
        self.user_id = user_id
        self.currency = currency
        self.amount = amount

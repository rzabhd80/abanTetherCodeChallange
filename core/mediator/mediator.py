from core.cqrs.base_cqrs import Request, Handler


class Mediator:
    def __init__(self):
        self.handlers = {}

    def register(self, request_type: type, handler: Handler):
        self.handlers[request_type] = handler

    async def send(self, request: Request):
        handler = self.handlers.get(type(request))
        if not handler:
            raise ValueError(f"No handler registered for {type(request)}")
        return await handler.handle(request)

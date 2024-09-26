from abc import ABC, abstractmethod


class Request(ABC):
    pass


class Handler(ABC):
    @abstractmethod
    async def handle(self, request: Request):
        pass


class Command(Request):
    pass


class Query(Request):
    pass

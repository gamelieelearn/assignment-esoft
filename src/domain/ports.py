from abc import ABC, abstractmethod
from typing import Any, List, Protocol


class MessageBus(ABC):
    @abstractmethod
    def receive(self, max_messages: int = 1) -> List[Any]: ...
    @abstractmethod
    def send(self, messages: List[Any]) -> None: ...


class ModelRunner(Protocol):
    def predict(self, batch): ...

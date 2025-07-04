from typing import Any, Protocol


class MessageBus(Protocol):
    def send(self, data: str | dict) -> str: ...
    def receive(self, max_messages: int = 1, wait_time_seconds: int = 5) -> list[dict]: ...
    def delete(self, message: dict) -> None: ...


class S3Compatible(Protocol):
    def store(self, key: str, data: Any, bucket: str) -> None: ...
    def retrieve(self, key: str, bucket: str) -> Any: ...


class ModelRunner(Protocol):
    def predict(self, batch: list[Any]) -> list[Any]: ...

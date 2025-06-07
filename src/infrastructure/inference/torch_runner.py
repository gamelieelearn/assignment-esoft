from abc import ABC, abstractmethod


class TorchRunner(ABC):
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def run(self, input_data): ...

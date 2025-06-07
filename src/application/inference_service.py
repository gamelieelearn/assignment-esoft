import json

from src.domain.ports import MessageBus, ModelRunner, S3Compatible


class InferenceService:
    def __init__(
        self,
        bus_in: MessageBus,
        storage: S3Compatible,
        bus_out: MessageBus,
        model: ModelRunner,
        batch=10,
    ):
        self.bus_in = bus_in
        self.storage = storage
        self.bus_out = bus_out
        self.model = model
        self.batch = batch

    def handle_batch(self, messages):
        payloads = [json.loads(m['Body']) for m in messages]
        predictions = self.model.predict(payloads)
        self.bus_out.send(predictions)

    def run_forever(self):
        while True:
            msgs = self.bus_in.receive(self.batch)
            self.handle_batch(msgs)

from src.domain.entities import InferOut, InputModel, OutputModel
from src.domain.ports import MessageBus, ModelRunner, S3Compatible


class InferenceService:
    def __init__(
        self,
        bus_in: MessageBus,
        s3: S3Compatible,
        bus_out: MessageBus,
        model: ModelRunner,
        batch=10,
    ):
        self.bus_in = bus_in
        self.s3 = s3
        self.bus_out = bus_out
        self.model = model
        self.batch = batch

    def handle_batch(self, raw_messages):
        # input validatation
        messages: list[InputModel] = []
        for m in raw_messages:
            messages.append(InputModel.model_validate(m))

        # download images from s3, can improve latency
        batch = []
        for m in messages:
            image_bytes: bytes = self.s3.retrieve(key=m.key, bucket=m.bucket)
            batch.append(image_bytes)

        # model predition
        predictions = self.model.predict(batch)

        # form the output and send
        for m, p in zip(messages, predictions):
            out = OutputModel(input=m, result=InferOut(class_name=p))
            self.bus_out.send(out.model_dump_json())

    def run_forever(self):
        while True:
            msgs = self.bus_in.receive(self.batch)
            self.handle_batch(msgs)

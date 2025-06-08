import time

from src.domain.entities import InferOut, InputModel, OutputModel
from src.domain.ports import MessageBus, ModelRunner, S3Compatible
from src.utils.otel import get_meter

meter = get_meter()

# Define metrics
batch_latency_hist = meter.create_histogram(
    name='inference_batch_latency_seconds',
    description='Time taken to process a batch of images (seconds)',
    unit='s',
)
throughput_counter = meter.create_counter(
    name='inference_images_processed_total',
    description='Total number of images processed',
    unit='1',
)


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
        start = time.perf_counter()
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

        # Record metrics
        elapsed = time.perf_counter() - start
        batch_latency_hist.record(elapsed)
        throughput_counter.add(len(messages))

    def run_forever(self):
        while True:
            msgs = self.bus_in.receive(self.batch)
            if len(msgs) == 0:
                print('No messages received, waiting...', flush=True)
                continue
            self.handle_batch(msgs)

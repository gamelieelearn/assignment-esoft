import time

from pydantic import BaseModel, Field

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

image_download_latency_hist = meter.create_histogram(
    name='inference_image_download_latency_seconds',
    description='Time taken to download all images in a batch from S3 (seconds)',
    unit='s',
)
inference_latency_hist = meter.create_histogram(
    name='inference_model_latency_seconds',
    description='Time taken for model inference on a batch (seconds)',
    unit='s',
)

batch_size_hist = meter.create_histogram(  # should use a gauge
    name='inference_batch_size',
    description='Number of images in each batch',
    unit='1',
)


class SQSMessage(BaseModel):
    body: InputModel = Field(..., alias='Body')
    receipt_handle: str = Field(..., alias='ReceiptHandle')


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
        messages: list[SQSMessage] = []
        for m in raw_messages:
            messages.append(SQSMessage.model_validate(m))
        batch_size_hist.record(len(messages))

        # download images from s3, can improve latency
        download_start = time.perf_counter()
        batch = []
        for m in messages:
            image_bytes: bytes = self.s3.retrieve(key=m.body.key, bucket=m.body.bucket)
            batch.append(image_bytes)
        download_elapsed = time.perf_counter() - download_start
        image_download_latency_hist.record(download_elapsed)

        # model prediction
        inference_start = time.perf_counter()
        predictions = self.model.predict(batch)
        inference_elapsed = time.perf_counter() - inference_start
        inference_latency_hist.record(inference_elapsed)

        # form the output and send
        for m, p in zip(messages, predictions):
            out = OutputModel(input=m.body, result=InferOut(class_name=p))
            self.bus_out.send(out.model_dump_json())

        elapsed = time.perf_counter() - start
        # Delete messages
        for m in messages:
            self.bus_in.delete(m.model_dump(by_alias=False))

        # Record metrics
        batch_latency_hist.record(elapsed)
        throughput_counter.add(len(messages))

    def run_forever(self):
        while True:
            msgs = self.bus_in.receive(self.batch)
            if len(msgs) == 0:
                print('No messages received, waiting...', flush=True)
                continue
            self.handle_batch(msgs)

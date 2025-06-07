from src.application.inference_service import InferenceService
from src.config.config import settings
from src.infrastructure.aws.s3 import StorageS3
from src.infrastructure.aws.sqs import SQSMessageBus
from src.infrastructure.inference.transformer_runner import SimpleTransformerRunner


def inference_app():
    bus_in = SQSMessageBus(
        settings.sqs_queue_url,
        settings.aws_access_key_id,
        settings.aws_secret_access_key,
        settings.aws_default_region,
    )
    bus_out = SQSMessageBus(
        settings.sqs_queue_url_out,
        settings.aws_access_key_id,
        settings.aws_secret_access_key,
        settings.aws_default_region,
    )
    s3 = StorageS3(
        settings.aws_access_key_id,
        settings.aws_secret_access_key,
        settings.aws_default_region,
    )
    model = SimpleTransformerRunner(settings.model_name)

    service = InferenceService(bus_in, s3, bus_out, model, batch=settings.batch)
    service.run_forever()

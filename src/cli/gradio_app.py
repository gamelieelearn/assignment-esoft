from src.application.gradio_service import GradioService
from src.config.config import settings
from src.infrastructure.aws.s3 import StorageS3
from src.infrastructure.aws.sqs import SQSMessageBus


def gradio_app():
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

    service = GradioService(bus_in, s3, bus_out, bucket_name=settings.bucket_name)
    service.run_forever()

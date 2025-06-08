from src.config.config import settings
from src.infrastructure.aws.sqs import SQSMessageBus


def clean_sqs_out():
    bus_out = SQSMessageBus(
        settings.sqs_queue_url_out,
        settings.aws_access_key_id,
        settings.aws_secret_access_key,
        settings.aws_default_region,
    )
    bus_out.purge()
    print('All messages purged from sqs_out queue.')

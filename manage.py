# pragma: no cover
import fire
import sentry_sdk

from src.cli import gradio_app, inference_app
from src.config.config import settings

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
    )
    print('Sentry initialized with DSN:', settings.sentry_dsn)


def main_inference_app():
    """Lauch inference service to process messages from SQS and perform model inference."""
    inference_app.inference_app()


def main_gradio_app():
    """Lauch gradio interface for image upload and inference results display."""
    gradio_app.gradio_app()


def main_clean_sqs_out():
    """Delete all messages in the sqs_out queue and display the number of messages deleted."""
    from src.cli import sqs_out_cleaner

    sqs_out_cleaner.clean_sqs_out()


if __name__ == '__main__':
    fire.Fire(
        {
            'inference': main_inference_app,
            'gradio': main_gradio_app,
            'clean_sqs_out': main_clean_sqs_out,
        }
    )

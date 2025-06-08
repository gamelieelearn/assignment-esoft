from dynaconf import Dynaconf


class MySettings(Dynaconf):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str
    sqs_queue_url: str
    sqs_queue_url_out: str
    bucket_name: str
    model_name: str
    batch: int
    sentry_dsn: str | None
    gradio_user: str | None
    gradio_password: str | None


settings = MySettings(
    settings_files=['settings.toml', '.secrets.toml'],
    environments=True,
    load_dotenv=True,
)

assert settings.sentry_dsn is not None

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


settings = MySettings(
    settings_files=['settings.toml', '.secrets.toml'],
    environments=True,
    load_dotenv=True,
)

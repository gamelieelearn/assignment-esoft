from dynaconf import Dynaconf


class MySettings(Dynaconf):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_default_region: str
    sqs_queue_url: str
    abc: str


settings = MySettings(
    settings_files=['settings.toml', '.secrets.toml'],
    environments=True,
    load_dotenv=True,
)

# assignment-esoft

A simple service with Gradio UI and Docker support.

## Links

- [Gradio Demo](https://gradio.sieubun.xyz)
- [Grafana Dashboard](https://assignmentesoft.grafana.net/public-dashboards/6663c2fcb6fe4b9099c0d659ef5d7965)

## Getting Started

### Setup Secrets

Before running locally, copy `.secrets.toml.example` to `.secrets.toml` and fill in your secrets:

```bash
cp .secrets.toml.example .secrets.toml
# Edit .secrets.toml with your credentials
```

When running with Docker, you can set secrets as environment variables with the `DYNACONF_` prefix, for example:

```bash
export DYNACONF_AWS_ACCESS_KEY_ID=your_key
export DYNACONF_AWS_SECRET_ACCESS_KEY=your_secret
```

### Run Locally

```bash
pip install -r requirements.txt
python manage.py inference
```

### Run with Docker

```bash
docker-compose build
docker-compose up -d
```

### Run Tests

```bash
pytest
```

### Configuration list

| Environment variable           | Meaning                                                          |
| ------------------------------ | ---------------------------------------------------------------- |
| DYNACONF_AWS_ACCESS_KEY_ID     | aws key id                                                       |
| DYNACONF_AWS_SECRET_ACCESS_KEY | aws access key                                                   |
| DYNACONF_AWS_DEFAULT_REGION    | aws default region                                               |
| DYNACONF_SQS_QUEUE_URL         | SQS queue with input messages                                    |
| DYNACONF_SQS_QUEUE_URL_OUT     | SQS queue output (input images with inference result)            |
| DYNACONF_BUCKET_NAME           | S3 bucket name (Only for Gradio and `python manage.py benchmark) |
| DYNACONF_MODEL_NAME            | Huggingface model name                                           |
| DYNACONF_BATCH                 | Inference batch size, maximum 10                                 |
| DYNACONF_GRADIO_USER           | Gradio default user                                              |
| DYNACONF_GRADIO_PASSWORD       | Gradio default password                                          |

---

For more options:

```bash
python manage.py --help
```

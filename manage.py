import fire

from src.cli import inference_app  # noqa: F401

if __name__ == '__main__':
    fire.Fire(
        {
            'inference_app': inference_app.inference_app(),
        }
    )

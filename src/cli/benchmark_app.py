import io

from datasets import load_dataset
from PIL import Image

from src.config.config import settings
from src.infrastructure.aws.s3 import StorageS3
from src.infrastructure.aws.sqs import SQSMessageBus


def benchmark_app(num_images: int = 10):
    dataset = load_dataset('microsoft/cats_vs_dogs', split='train').shuffle(seed=42)

    bus_in = SQSMessageBus(
        settings.sqs_queue_url,
        settings.aws_access_key_id,
        settings.aws_secret_access_key,
        settings.aws_default_region,
    )
    s3 = StorageS3(
        settings.aws_access_key_id,
        settings.aws_secret_access_key,
        settings.aws_default_region,
    )
    bucket = settings.bucket_name

    count = 0
    for item in dataset:
        if count >= num_images:
            break
        image = item['image']
        if not isinstance(image, Image.Image):
            continue
        # Save image to bytes
        buf = io.BytesIO()
        image.save(buf, format='JPEG')
        img_bytes = buf.getvalue()
        key = f'benchmark/{count}.jpg'
        s3.store(key, img_bytes, bucket)
        bus_in.send({'bucket': bucket, 'key': key})
        print(f'Sent image {count + 1}/{num_images} to SQS and S3: {key}')
        count += 1
    print(f'Benchmarking complete. {count} images sent.')

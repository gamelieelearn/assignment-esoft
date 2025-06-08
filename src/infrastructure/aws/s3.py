from typing import Any

import boto3
from botocore.exceptions import NoCredentialsError


class StorageS3:
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_default_region: str,
    ):
        self.client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_default_region,
        )

    def store(self, key: str, data: Any, bucket: str) -> None:
        try:
            self.client.put_object(Bucket=bucket, Key=key, Body=data)
            print(f'Upload successful! Bucket: {bucket}, Key: {key}', flush=True)
        except NoCredentialsError:
            print('Credentials not available.')
        except Exception as e:
            print(f'Upload failed: {e}')

    def retrieve(self, key: str, bucket: str) -> Any:
        try:
            response = self.client.get_object(Bucket=bucket, Key=key)
            data = response['Body'].read()
            print(f'Download successful! Bucket: {bucket}, Key: {key}', flush=True)
            return data
        except NoCredentialsError:
            print('Credentials not available.')
        except Exception as e:
            print(f'Download failed: {e}')


if __name__ == '__main__':
    import os

    import requests

    from src.config.config import settings

    image_path = 'test/artifacts/example_image.jpg'

    if not os.path.exists(image_path):
        url = 'https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg'
        img_data = requests.get(url).content
        with open(image_path, 'wb') as handler:
            handler.write(img_data)
        print(f'Downloaded example image to {image_path}')
    s3_key = 'tmpbl_6dq9u.jpg'

    s3_client = StorageS3(
        settings.aws_access_key_id,
        settings.aws_secret_access_key,
        settings.aws_default_region,
    )

    with open(image_path, 'rb') as f:
        img_bytes = f.read()
    s3_client.store(s3_key, img_bytes, settings.bucket_name)
    downloaded_bytes = s3_client.retrieve(s3_key, settings.bucket_name)
    download_path = '/tmp/downloaded_example_image.jpg'
    if downloaded_bytes:
        with open(download_path, 'wb') as f:
            f.write(downloaded_bytes)
        print(f'Saved downloaded image to {download_path}')

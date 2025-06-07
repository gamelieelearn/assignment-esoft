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

    def upload_image_to_s3(self, image_path, bucket, key):
        try:
            self.client.upload_file(image_path, bucket, key)
            print(f'Upload successful! Bucket: {bucket}, Key: {key}')
            return bucket, key
        except FileNotFoundError:
            print('The file was not found.')
        except NoCredentialsError:
            print('Credentials not available.')

    def download_image_from_s3(self, bucket, key, download_path):
        try:
            self.client.download_file(bucket, key, download_path)
            print(f'Download successful! Bucket: {bucket}, Key: {key}, Saved to: {download_path}')
            return download_path
        except FileNotFoundError:
            print('The download path was not found.')
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

    sqs_queue = StorageS3(
        settings.aws_access_key_id,
        settings.aws_secret_access_key,
        settings.aws_default_region,
    )
    sqs_queue.upload_image_to_s3(image_path, settings.bucket_name, s3_key)
    download_path = '/tmp/downloaded_example_image.jpg'
    sqs_queue.download_image_from_s3(settings.bucket_name, s3_key, download_path)

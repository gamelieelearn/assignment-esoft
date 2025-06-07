import boto3
from moto import mock_aws

from src.infrastructure.aws.s3 import StorageS3


@mock_aws
class TestStorageS3:
    def test_store(self):
        # Arrange
        conn = boto3.resource('s3', region_name='us-east-1')
        bucket = 'not-a-bucket'
        conn.create_bucket(Bucket=bucket)
        # Act
        model_instance = StorageS3(
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
            aws_default_region='us-east-1',
        )
        model_instance.store(key='steve', data='is awesome', bucket=bucket)
        # Assert
        body = conn.Object(bucket, 'steve').get()['Body'].read().decode('utf-8')

        assert body == 'is awesome'

    def test_retrieve(self):
        # Arrange
        conn = boto3.resource('s3', region_name='us-east-1')
        bucket = 'not-a-bucket'
        conn.create_bucket(Bucket=bucket)
        conn.Object(bucket, 'steve').put(Body='hello world')
        # Act
        model_instance = StorageS3(
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
            aws_default_region='us-east-1',
        )
        data = model_instance.retrieve(key='steve', bucket=bucket)
        # Assert

        assert data.decode('utf-8') == 'hello world'

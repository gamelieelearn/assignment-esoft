from typing import Any
from unittest.mock import MagicMock

import boto3
from moto import mock_aws

from src.application.inference_service import InferenceService


@mock_aws
class TestInferenceService:
    def test_handle_batch(self):
        # Arrange
        fake_input = {'Body': {'bucket': 'test-bucket', 'key': 'test-key'}, 'ReceiptHandle': 'none'}
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='test-key', Body=b'imgbytes')

        # Mock S3Compatible to use moto
        class S3CompatibleMoto:
            def store(self, key: str, data: Any, bucket: str) -> None: ...

            def retrieve(self, key, bucket):
                obj = s3.get_object(Bucket=bucket, Key=key)
                return obj['Body'].read()

        bus_in = MagicMock()
        bus_out = MagicMock()
        model = MagicMock()
        model.predict.return_value = ['cat']
        service = InferenceService(bus_in, S3CompatibleMoto(), bus_out, model, batch=1)

        # Use InputModel to validate input
        raw_messages = [fake_input]
        service.handle_batch(raw_messages)

        model.predict.assert_called_once_with([b'imgbytes'])
        assert bus_out.send.call_count == 1
        # Optionally, check the output format
        sent_json = bus_out.send.call_args[0][0]
        assert 'cat' in sent_json

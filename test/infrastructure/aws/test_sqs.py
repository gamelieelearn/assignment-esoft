import boto3
from moto import mock_aws

from src.infrastructure.aws.sqs import SQSMessageBus


@mock_aws
class TestSQSMessageBus:
    def setup_method(self, method):
        self.sqs = boto3.client('sqs', region_name='us-east-1')
        response = self.sqs.create_queue(QueueName='test-queue')
        self.queue_url = response['QueueUrl']
        self.bus = SQSMessageBus(
            queue_url=self.queue_url,
            aws_access_key_id='fake_access_key',
            aws_secret_access_key='fake_secret_key',
            aws_default_region='us-east-1',
        )

    def test_send(self):
        # Act
        msg_id = self.bus.send({'foo': 'bar'})
        # Assert
        assert isinstance(msg_id, str)

    def test_receive(self):
        # Arrange
        self.bus.send({'hello': 'world'})
        # Act
        messages = self.bus.receive()
        # Assert
        assert isinstance(messages, list)
        assert messages[0]['hello'] == 'world'

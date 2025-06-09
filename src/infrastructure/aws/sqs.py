import json

import boto3


class SQSMessageBus:
    def __init__(
        self,
        queue_url: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_default_region: str,
    ):
        self.queue_url = queue_url
        self.client = boto3.client(
            'sqs',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_default_region,
        )

    def send(self, data: str | dict) -> str:
        if isinstance(data, dict):
            data = json.dumps(data)
        response = self.client.send_message(QueueUrl=self.queue_url, MessageBody=data)
        print(f'Message sent to SQS! MessageId: {response["MessageId"]}', flush=True)
        return response['MessageId']

    def receive(self, max_messages: int = 1, wait_time_seconds: int = 5) -> list[dict]:
        """Poll messages from SQS queue"""
        response = self.client.receive_message(
            QueueUrl=self.queue_url, MaxNumberOfMessages=max_messages, WaitTimeSeconds=wait_time_seconds
        )
        messages = response.get('Messages', [])
        return messages

    def purge(self):
        self.client.purge_queue(QueueUrl=self.queue_url)
        print(f'Queue {self.queue_url} purged.', flush=True)

    def delete(self, message: dict) -> None:
        """Pass the message received from SQS to delete it."""
        receipt_handle = message.get('ReceiptHandle') or message.get('receipt_handle')
        self.client.delete_message(QueueUrl=self.queue_url, ReceiptHandle=receipt_handle)
        print('Message deleted from SQS queue.', flush=True)


if __name__ == '__main__':
    from src.config.config import settings

    sqs_queue = SQSMessageBus(
        settings.sqs_queue_url,
        settings.aws_access_key_id,
        settings.aws_secret_access_key,
        settings.aws_default_region,
    )

    sqs_queue.send(json.dumps({'s3_key': 'this_is_an_image.jpg', 'bucket_name': 'my-bucket'}))
    messages = sqs_queue.receive(wait_time_seconds=20)
    print(f'{messages=}')

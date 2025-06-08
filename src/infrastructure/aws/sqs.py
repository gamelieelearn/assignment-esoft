import json
import os

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

    def send(self, message):
        """message should be json serializable"""

        try:
            response = self.client.send_message(QueueUrl=self.queue_url, MessageBody=json.dumps(message))
        except Exception as e:
            print(f'{self.queue_url=}')
            raise e
        print(f'Message sent to SQS! MessageId: {response["MessageId"]}', flush=True)
        return response['MessageId']

    def receive(self, max_messages=1, wait_time_seconds=5, delete_after_polling=True):
        """Poll messages from SQS queue"""
        response = self.client.receive_message(
            QueueUrl=self.queue_url, MaxNumberOfMessages=max_messages, WaitTimeSeconds=wait_time_seconds
        )
        messages = response.get('Messages', [])
        if not messages:
            print('No messages received.')
            return []
        message = messages[0]
        body = json.loads(message['Body'])
        print(f'Received message: {body}', flush=True)
        # Optionally delete the message from the queue
        if delete_after_polling:
            self.client.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message['ReceiptHandle'])
            print('Message deleted from SQS queue.', flush=True)
        return [body]

    def purge(self):
        self.client.purge_queue(QueueUrl=self.queue_url)
        print(f'Queue {self.queue_url} purged.', flush=True)


if __name__ == '__main__':
    from src.config.config import settings

    S3_KEY = os.getenv('S3_KEY', 'tmpbl_6dq9u.jpg')
    sqs_queue = SQSMessageBus(
        settings.sqs_queue_url,
        settings.aws_access_key_id,
        settings.aws_secret_access_key,
        settings.aws_default_region,
    )
    sqs_queue.send({'s3_key': 'this_is_an_image.jpg', 'bucket_name': 'my-bucket'})
    sqs_queue.receive()

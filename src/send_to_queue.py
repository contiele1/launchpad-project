import boto3
import json


def send_to_queue(messages: list):

    sqs = boto3.client("sqs", region_name="eu-west-2")

    queue_url = "https://sqs.eu-west-2.amazonaws.com/522585361178/FirstQueue"

    for message in messages:
        message = json.dumps(message)
        response = sqs.send_message(QueueUrl=queue_url, MessageBody=message)
        print(response["MessageId"])

import requests
import boto3
import json


def call_api(api_key: str, content: str = None, date: str = None):

    URL = "https://content.guardianapis.com/search"

    params = {"q": content, "from-date": date, "order-by": "newest", "api-key": api_key}

    response = requests.get(url=URL, params=params)

    print(response)

    results = response.json()
    selected_results = [
        {
            "webPublicationDate": result["webPublicationDate"],
            "webTitle": result["webTitle"],
            "webUrl": result["webUrl"],
        }
        for result in results["response"]["results"]
    ]
    return selected_results


def send_to_queue(messages: list):

    sqs = boto3.client("sqs", region_name="eu-west-2")

    queue_url = sqs.get_queue_url(QueueName="guardian_content")["QueueUrl"]

    for message in messages:
        message = json.dumps(message)
        response = sqs.send_message(QueueUrl=queue_url, MessageBody=message)
        print(response["MessageId"])


def lambda_handler(event, context):
    api_key = event.get("api_key")
    content = event.get("content")
    date = event.get("date")
    messages = call_api(api_key, content, date)
    send_to_queue(messages)

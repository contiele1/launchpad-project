from typing import Any, Optional
import requests
import boto3
import json

GUARDIANAPIS_URL = "https://content.guardianapis.com/search"


def call_api(
    api_key: str, content: str, date: str = None, debug: bool = True
) -> Optional[list[dict[str, Any]]]:
    """Make a call to the Guardian search API.

    Args:
        api_key (str): API key for guardianpapis.com
        content (str): Keyword to search
        date (str): Date to start search from
        debug (bool, optional): Print debug info. Defaults to True.

    Returns:
        Optional[list[dict[str, Any]]]: A list of relevant searches, or None
        if something went wrong.
    """

    params = {"q": content, "from-date": date, "order-by": "newest", "api-key": api_key}
    response = requests.get(url=GUARDIANAPIS_URL, params=params)
    print(response.url)

    if response.status_code != 200:
        print(f"Failed to get response: {response.status_code=}")
        return None

    if debug:
        print(response)

    selected_results = process_response_json(response.json())

    if not selected_results:
        print(f"No results found for keyword {content}")
        return None

    return selected_results


def process_response_json(response_json: dict[str, Any]) -> list[dict[str, Any]]:
    if "response" not in response_json:
        print("No 'response' in returned JSON")
        return []
    if "results" not in response_json["response"]:
        print("No 'results' in returned JSON")
        return []
    results = response_json["response"]["results"]
    return [
        {
            "webPublicationDate": result["webPublicationDate"],
            "webTitle": result["webTitle"],
            "webUrl": result["webUrl"],
        }
        for result in results
    ]


def send_to_queue(messages: list):
    sqs = boto3.client("sqs", region_name="eu-west-2")
    queue_url = sqs.get_queue_url(QueueName="guardian_content")["QueueUrl"]
    message_Ids = []
    for message in messages:
        message = json.dumps(message)
        response = sqs.send_message(QueueUrl=queue_url, MessageBody=message)
        print(response["MessageId"])
        message_Ids.append(response["MessageId"])
    return message_Ids


def lambda_handler(event, context):
    def required_contents(key: str) -> str:
        if value := event.get(key):
            return value
        else:
            raise ValueError(f"A required key is missing from event: {key}")

    api_key = required_contents("api_key")
    content = required_contents("content")
    date = event.get("date")

    if messages := call_api(api_key, content, date):
        send_to_queue(messages)
    else:
        print("No messages to send to queue")

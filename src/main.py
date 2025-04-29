import requests
import pprint
import boto3
import json
from dotenv import load_dotenv
import os



def call_api(api_key: str, content:str = None, date:str = None):

    URL = "https://content.guardianapis.com/search"

    params = {"q":content,
            "from-date": date,
            "order-by":"newest",
            "api-key":api_key}

    response = requests.get(url=URL,params=params)

    print(response)

    results = response.json()
    selected_results = [{"webPublicationDate":result["webPublicationDate"],
                         "webTitle":result["webTitle"],
                         "webUrl":result["webUrl"]} 
                         for result in results['response']['results']]

    return selected_results



def send_to_queue(messages: list):
            
        sqs = boto3.client("sqs", region_name="eu-west-2")

        queue_url = "https://sqs.eu-west-2.amazonaws.com/522585361178/FirstQueue"

        for message in messages:
                message = json.dumps(message)
                response = sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=message
                    ) 
                print(response['MessageId'])




if __name__ == "__main__":
        
        load_dotenv()
        api_key = os.environ["API-KEY"]

        messages = call_api(api_key, "chess")
        
        send_to_queue(messages)
        
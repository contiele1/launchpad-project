import requests


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


def call_lambda_handler(event,context):
    api_key = event.get("api_key")
    content = event.get("content")
    date = event.get("date")
    
    return call_api(api_key, content, date)

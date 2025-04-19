import requests
import pprint


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

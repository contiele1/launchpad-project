from dotenv import load_dotenv
import os
import requests
import pprint

load_dotenv()

URL = "https://content.guardianapis.com/search"


params = {"q":"chess",
          "order-by":"newest",
          "api-key":os.environ["API-KEY"]}

response = requests.get(url=URL,params=params)

print(response)

results = response.json()
selected_results = [{"webPublicationDate":result["webPublicationDate"],"webTitle":result["webTitle"],"webUrl":result["webUrl"]} for result in results['response']['results']]

pprint.pp(selected_results)

# pprint.pp(data['response']['results'][0])
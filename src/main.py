import requests
import pprint

URL = "https://content.guardianapis.com/search"

apikey = "27691256-07ee-4414-96b7-90b4c4c4ae27"

params = {"q":"chess",
          "api-key":"test"}

response = requests.get(url=URL,params=params)

print(response)
#print(response.__attrs__)


data = response.json()
# pprint.pp(data)
pprint.pp(data['response']['results'][0])
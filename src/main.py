import requests

URL = "https://content.guardianapis.com/search?q=debates"

apikey = "27691256-07ee-4414-96b7-90b4c4c4ae27"
test_apykey = "test"

response = requests.get(URL+"&api-key="+test_apykey)

print(response)

data = response.json()

print(data)
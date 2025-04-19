from src.main import call_api
from dotenv import load_dotenv
import os
import pprint

# $env:PYTHONPATH = $PWD



load_dotenv()
api_key = os.environ["API-KEY"]


class TestCallApi:
    def test_call_api_returns_10_results(self):
        selected_results = call_api(api_key=api_key, content="Milan")
        pprint.pp(selected_results)
        assert len(selected_results) == 10
from src.main import call_api
import unittest
from dotenv import load_dotenv
import os
import pprint

# $env:PYTHONPATH = $PWD



load_dotenv()
api_key = os.environ["API-KEY"]


class TestCallApi(unittest.TestCase):

    @unittest.skip("skip test")
    def test_call_api_returns_10_results(self):
        selected_results = call_api(api_key=api_key, content="Milan")
        assert len(selected_results) == 10
        selected_results = call_api(api_key=api_key,content="Manchester")
        assert len(selected_results) == 10
        pprint.pp(selected_results)
    
    @unittest.skip("skip test")
    def test_call_api_returns_results_according_to_content_request(self):
        selected_results_1 = call_api(api_key=api_key, content="Milan")
        selected_results_2 = call_api(api_key=api_key, content="Manchester")
        selected_results_3 = call_api(api_key=api_key, content="Milan")
        assert selected_results_1 != selected_results_2
        assert selected_results_1 == selected_results_3

    # @unittest.skip("skip test")
    def test_call_api_returns_results_after_specified_date(self):
        selected_results_no_date = call_api(api_key=api_key,content="Alberto")
        pprint.pp(selected_results_no_date)
        assert all(result["webPublicationDate"]>"2025-04-15" for result in selected_results_no_date) == False
        selected_results_with_date = call_api(api_key=api_key, content= "Alberto", date="2025-04-15")
        pprint.pp(selected_results_with_date)
        assert all(result["webPublicationDate"]>"2025-04-15" for result in selected_results_with_date) == True
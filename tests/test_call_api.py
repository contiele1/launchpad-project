from src.main import call_api, process_response_json, send_to_queue, lambda_handler
import pytest
from unittest.mock import patch, MagicMock
import json
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.environ["API-KEY"]


def get_test_data():
    with open("tests/resources/query_result.json", "r") as f:
        return json.load(f)


response_json = get_test_data()


class TestProcessResponseJSON:

    def test_function_returns_list_of_dicts(self):
        processed_response = process_response_json(response_json)
        assert type(processed_response) == list
        assert all(type(content) == dict for content in processed_response)

    def test_function_returns_list_of_dicts_with_right_format(self):
        processed_response = process_response_json(response_json)
        assert all(len(content) == 3 for content in processed_response)
        assert all(content.get("webPublicationDate") for content in processed_response)
        assert all(content.get("webTitle") for content in processed_response)
        assert all(content.get("webUrl") for content in processed_response)


class TestCallApi:
    @patch("requests.get")
    def test_function_returns_None_if_error(self, mock_get):
        mock_get.return_value.status_code = 201
        mock_get.return_value.json.return_value = response_json
        selected_results = call_api(api_key="test", content="foo")
        assert selected_results == None

    @patch("requests.get")
    @patch("src.main.process_response_json")
    def test_function_call_process_funct_and_returns_selected_results(
        self, mock_process, mock_get
    ):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = response_json
        mock_process.return_value = process_response_json(response_json)
        selected_results = call_api(api_key="test", content="foo")

        mock_process.assert_called_once_with(response_json)
        assert selected_results == process_response_json(response_json)


class TestSendToQueue:
    @patch("boto3.client")
    def test_function_calls_sqs_client_for_every_message(self, mock_boto_client):
        mock_sqs = MagicMock()
        mock_boto_client.return_value = mock_sqs
        mock_sqs.send_message.return_value = {"MessageId": "id"}
        message_Ids = send_to_queue(["message1", "message2"])
        assert message_Ids == ["id", "id"]
        message_Ids = send_to_queue(["message1", "message2", "message3"])
        assert message_Ids == ["id", "id", "id"]


class TestLambdaHandler:
    def test_function_raises_value_error_if_key_missing(self):
        event = {"content": "Harry Potter"}
        with pytest.raises(ValueError):
            lambda_handler(event, {})
        event = {"api_key": "foo"}
        with pytest.raises(ValueError):
            lambda_handler(event, {})

    @patch("src.main.call_api")
    @patch("src.main.send_to_queue")
    def test_function_calls_call_api_and_send_to_queue(self, mock_send, mock_call):
        event = {"content": "Harry Potter", "api_key": "foo"}
        mock_call.return_value = "Article on Harry Potter"
        lambda_handler(event, {})
        mock_call.assert_called_once_with("foo", "Harry Potter", None)
        mock_send.assert_called_once_with("Article on Harry Potter")

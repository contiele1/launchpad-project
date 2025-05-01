from src.call_api import call_api
from src.send_to_queue import send_to_queue
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.environ["API-KEY"]

messages = call_api(api_key, "chess")

print(messages)

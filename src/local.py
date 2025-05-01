from src.main import lambda_handler
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.environ["API-KEY"]

lambda_handler({"api_key":api_key},{})


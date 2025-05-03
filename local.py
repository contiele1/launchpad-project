from datetime import datetime
import time
from src.main import lambda_handler
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    while True:
        content = input("Please insert a search term: ")
        if content:
            break
    while True:
        date = input("If you want, insert a starting date for your search (dd-mm-yyyy), otherwise simply press Enter: ")
        def is_dd_mm_yyyy_format(date_str: str) -> bool:
            try:
                datetime.strptime(date_str, "%d-%m-%Y")
                return True
            except ValueError:
                return False
        if is_dd_mm_yyyy_format(date):
            date_obj = datetime.strptime(date, "%d-%m-%Y")
            date = date_obj.strftime("%Y-%m-%d")
            break
        if date == "":
            date = None
            break
        else:
            print("Wrong date format.")
            time.sleep(1)
           
    load_dotenv()
    api_key = os.environ["API-KEY"]
    event = {
        "content": content,
        "api_key": api_key,
        "date": date
    }
    lambda_handler(event, {})

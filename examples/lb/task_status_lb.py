import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

# Load env
load_dotenv()
api_key = os.getenv("API_KEY")

# Init client
client = KrutrimClient(api_key=api_key)
try:
    resp = client.lb.get_task_status(
        x_region = "enter the x_region",
        task_id="enter the task id here"
    )
    print(f"Task status: {resp}")


except Exception as e:
    print(f"Error has occurred: {e}")
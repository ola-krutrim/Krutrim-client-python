from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")

client = KrutrimClient(api_key=api_key)

try:
    # GET /vm/v1/get_instance_task_status?task_id=...
    get_instance_task_status_resp = client.highlvlvpc.get_instance_task_status(
        task_id="enter the task id",
    )

    print(f"Get instance task status executed successfully : {get_instance_task_status_resp}")

except Exception as e:
    print(f"Exception  {e}")

from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # GET /vm/v1/instance-templates/list?page=1&limit=10
    templates = client.highlvlvpc.list_instance_templates(
        x_region="enter the region name",
        # x_region possible values "In-Bangalore-1","In-Hyderabad-1"
        page=1,
        limit=10,
    )
    print(f"Templates: {templates}")

except Exception as e:
    print(f"Exception occurred: {e}")

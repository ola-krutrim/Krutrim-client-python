from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # GET /kbs/v1/volumes
    volumes = client.kbs.list_volumes(
        k_tenant_id="enter the VPC KRN",
        x_region="enter the region name",
        # x_region possible values "In-Bangalore-1","In-Hyderabad-1"
    )
    print(f"Volumes: {volumes}")

except Exception as e:
    print(f"Exception occurred: {e}")

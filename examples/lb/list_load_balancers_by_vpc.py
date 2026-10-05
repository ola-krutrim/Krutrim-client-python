import os

from dotenv import load_dotenv

from krutrim_client import KrutrimClient

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # GET /api/v3/loadbalancer/getallbyvpc?vpc_krn=...
    resp = client.lb.list_load_balancers_by_vpc(
        vpc_krn="enter the vpc krn",
        x_region="enter the region name",
        # x_region possible values: "In-Bangalore-1", "In-Hyderabad-1"
    )
    print(f"Load balancers: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

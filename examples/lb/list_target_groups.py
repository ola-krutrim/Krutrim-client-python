import os

from dotenv import load_dotenv

from krutrim_client import KrutrimClient

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # GET /api/v3/loadBalancer/targetgroups?vpc_krn=...
    resp = client.lb.list_target_groups(
        vpc_krn="enter the vpc krn",
        k_customer_id="enter the customer id",
        x_account_id="enter the account id",
        x_region="enter the region name",
        # x_region possible values: "In-Bangalore-1", "In-Hyderabad-1"
    )
    print(f"Target groups: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

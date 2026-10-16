import os

from dotenv import load_dotenv

from krutrim_client import KrutrimClient

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # DELETE /api/v3/loadBalancer/targetgroup/{target_group_krn}
    resp = client.lb.delete_target_group(
        "enter the target group krn",
        k_customer_id="enter the customer id",
        x_account_id="enter the account id",
        x_region="enter the region name",
        # x_region possible values: "In-Bangalore-1", "In-Hyderabad-1"
    )
    print(f"Delete target group result: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

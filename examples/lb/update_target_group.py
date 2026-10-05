import os

from dotenv import load_dotenv

from krutrim_client import KrutrimClient

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # PUT /api/v3/loadBalancer/targetgroup/{target_group_krn}
    resp = client.lb.update_target_group(
        "enter the target group krn",
        members=[
            {
                "name": "enter the member name",
                "weight": 1,
                "address": "enter the member IP address",
                "protocol_port": 700,
            }
        ],
        health_monitor={
            "delay": 10,
            "timeout": 5,
            "max_retries": 2,
            "health_check_path": "/",
            "name": "enter the health monitor name",
        },
        k_customer_id="enter the customer id",
        x_account_id="enter the account id",
        x_region="enter the region name",
        # x_region possible values: "In-Bangalore-1", "In-Hyderabad-1"
    )
    print(f"Update target group result: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

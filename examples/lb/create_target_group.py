import os

from dotenv import load_dotenv

from krutrim_client import KrutrimClient

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # POST /api/v3/loadBalancer/targetgroup
    resp = client.lb.create_target_group(
        target_group_name="enter the target group name",
        vpc_krn="enter the vpc krn",
        lb_krn=["enter the load balancer krn"],
        members=[
            {
                "name": "enter the member name",
                "address": "enter the member IP address",
                "protocol_port": 700,
                "weight": 1,
            }
        ],
        health_monitor={
            "delay": 10,
            "timeout": 5,
            "max_retries": 3,
            "health_check_path": "/",
            "type": "HTTP",
            "name": "enter the health monitor name",
        },
        k_customer_id="enter the customer id",
        x_account_id="enter the account id",
        x_region="enter the region name",
        # x_region possible values: "In-Bangalore-1", "In-Hyderabad-1"
    )
    print(f"Create target group result: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

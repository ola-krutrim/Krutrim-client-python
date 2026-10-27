import os

from dotenv import load_dotenv

from krutrim_client import KrutrimClient

load_dotenv()

api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key, environment="cloudx")

try:
    # POST /api/v3/loadbalancer/listener
    add_listener = client.lb.with_raw_response.add_listener(
        loadbalancer_krn="enter the load balancer krn",
        listener={
            "name": "http-listener",
            "protocol": "HTTP",
            "protocol_port": 8080,
            "default_pool": True,
            "pool_data": [
                {
                    "name": "backend-pool",
                    "description": "",
                    "algorithm": "ROUND_ROBIN",
                    "protocol": "HTTP",
                    "target_group_name": "enter the target group name",
                }
            ],
            "l7_policies": [],
        },
        k_customer_id="enter the customer id",
        x_account_id="enter the account id",
        # Must match the region embedded in loadbalancer_krn
        x_region="In-Hyderabad-2",
    )

    print(f"Successfully added listener {add_listener.json()}")

except Exception as e:
    print(f"Exception: {e}")

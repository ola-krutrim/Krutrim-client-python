from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key, environment="cloudx")

try:
    # PUT /api/v3/loadbalancer; the load balancer KRN is sent in the JSON body.
    update_load_balancer = client.lb.with_raw_response.update_load_balancer(
        lb_krn = "enter the load balancer krn",
        x_region = "In-Hyderabad-2",
        k_customer_id = "enter the customer id",
        x_account_id = "enter the account id",
        listener_krn = "enter the listener krn",
        listener = {"operation": "update", "name": "web"},
        pool = [
            {
                "krn": "enter the pool krn",
                "name": "poolx",
                "algorithm": "ROUND_ROBIN",
                "target_group_krn": "enter the target group krn",
            }
        ],
        policy = [
            {
                "operation": "update",
                "krn": "enter the policy krn",
                "name": "api",
                "action": "REDIRECT_TO_POOL",
                "redirect_pool_name": "poolx",
            }
        ],
        rules = [
            {
                "operation": "update",
                "krn": "enter the rule krn",
                "policy_krn": "enter the policy krn",
                "rule_type": "PATH",
                "compare_type": "EQUAL_TO",
                "value": "api",
            }
        ],
    )

    print(f"Successfully updated the load balancer {update_load_balancer.json()}")

except Exception as e:
    print(f"Exception: {e}")

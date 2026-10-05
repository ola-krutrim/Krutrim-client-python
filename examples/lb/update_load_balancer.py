import os

from dotenv import load_dotenv

from krutrim_client import KrutrimClient

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # PUT /api/v3/loadbalancer/{lb_krn}
    resp = client.lb.update_load_balancer(
        "enter the load balancer krn",
        x_region="enter the region name",
        # x_region possible values: "In-Bangalore-1", "In-Hyderabad-1"
        listener_krn="enter the listener krn",
        listener={
            "operation": "update",
            "name": "enter the updated listener name",
            "sni_container_refs": ["enter the certificate reference"],
        },
        loadbalancer={
            "description": "enter the updated load balancer description",
            "security_group_krn": ["enter the security group krn"],
        },
        policy=[
            {
                "operation": "create",
                "name": "enter the policy name",
                "action": "REDIRECT_TO_URL",
                "description": "enter the policy description",
                "redirect_url": "https://example.com/new-path",
                "redirect_http_code": 302,
                "position": 2,
                "admin_state_up": True,
                "tags": ["enter a tag"],
            }
        ],
        rules=[
            {
                "operation": "create",
                "policy_krn": "enter the policy krn",
                "rule_type": "HEADER",
                "compare_type": "EQUAL_TO",
                "key": "x-custom-header",
                "value": "true",
            }
        ],
        pool=[
            {
                "krn": "enter the pool krn",
                "name": "enter the pool name",
                "algorithm": "SOURCE_IP",
                "target_group_krn": "enter the target group krn",
            }
        ],
    )
    print(f"Update load balancer result: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

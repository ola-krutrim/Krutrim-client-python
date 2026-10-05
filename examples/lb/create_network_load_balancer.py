import os

from dotenv import load_dotenv

from krutrim_client import KrutrimClient

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # POST /api/v3/loadbalancer
    resp = client.lb.create_load_balancer(
        k_customer_id="enter the customer id",
        x_account_id="enter the account id",
        x_region="enter the region name",
        # x_region possible values: "In-Bangalore-1", "In-Hyderabad-1"
        loadbalancer_data={
            "name": "enter the load balancer name",
            "description": "enter the load balancer description",
            "floating_ip": False,
            "vpc_id": "enter the vpc krn",
            "network_id": "enter the network krn",
            "vip_subnet_id": "enter the subnet krn",
            "type": "NLB",
            "flavor": "standard",
            "security_group_krns": ["enter the security group krn"],
            "listeners": [
                {
                    "name": "enter the listener name",
                    "protocol": "TCP",
                    "protocol_port": 80,
                    "default_pool": True,
                    "pool_data": [
                        {
                            "name": "enter the pool name",
                            "description": "enter the pool description",
                            "algorithm": "ROUND_ROBIN",
                            "protocol": "TCP",
                            "target_group_name": "enter the target group name",
                        }
                    ],
                    "l7_policies": [],
                }
            ],
        },
    )
    print(f"Create network load balancer result: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

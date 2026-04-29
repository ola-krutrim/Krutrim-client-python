from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")

client = KrutrimClient(api_key=api_key)

try:
    raw_response = client.highlvlvpc.with_raw_response.create_subnet(
        subnet_data={
            "cidr": "enter the cidr",
            "gateway_ip": "enter the gateway ip",
            "name": "enter the name",
            "description": "enter the description",
            "ip_version": 4,
            "ingress": True,
            "egress": True,
            "network_id": "enter the network id",
        },
        vpc_id="enter the vpcid",
        x_region="enter the region",
        timeout=1000,
    )

    print("JSON response:", raw_response.http_response.json())

except Exception as e:
    print(f"Exception: {e}")
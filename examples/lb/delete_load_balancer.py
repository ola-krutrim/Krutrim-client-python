import os

from dotenv import load_dotenv

from krutrim_client import KrutrimClient

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # DELETE /api/v3/loadbalancer/{lb_krn}
    resp = client.lb.delete_load_balancer(
        "enter the load balancer krn",
        x_region="enter the region name",
        # x_region possible values: "In-Bangalore-1", "In-Hyderabad-1"
    )
    print(f"Delete load balancer result: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

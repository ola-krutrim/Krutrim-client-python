from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # DELETE /v1/highlvlvpc/detachFloatingIp/{port_krn}
    resp = client.highlvlvpc.detach_floating_ip(
        port_krn="enter the port krn",
        x_region="enter the region name",
        # x_region possible values "In-Bangalore-1","In-Hyderabad-1"
    )
    print(f"Detach result: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

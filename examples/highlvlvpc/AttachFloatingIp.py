from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # POST /v1/highlvlvpc/attachFloatingIp
    # Moves / attaches floating IP: detach from detach_port, attach to attach_port
    resp = client.highlvlvpc.attach_floating_ip(
        attach_port="enter the port krn to attach to",
        detach_port="enter the port krn to detach from",
        x_region="enter the region name",
        # x_region possible values "In-Bangalore-1","In-Hyderabad-1"
    )
    print(f"Attach result: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

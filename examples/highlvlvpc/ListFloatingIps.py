from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # GET /v1/highlvlvpc/floating_ip_list?vpc_id=...
    floating_ips = client.highlvlvpc.list_floating_ips(
        vpc_id="enter the vpc krn",
        x_region="enter the region name",
        # x_region possible values "In-Bangalore-1","In-Hyderabad-1"
    )
    print(f"Floating IPs: {floating_ips}")
    for item in floating_ips:
        print(item.floating_ip_address, item.port_krn, item.vm_name)

except Exception as e:
    print(f"Exception occurred: {e}")

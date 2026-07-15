from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # PUT /api/v1/ports/{port_krn}
    # Replaces the port's security group list with the one you pass.
    resp = client.highlvlvpc.update_port_security_groups(
        "enter the port KRN",
        security_groups=[
            "enter security group KRN 1",
            # "enter security group KRN 2",
        ],
        x_region="enter the region name",
        # x_region possible values "In-Bangalore-1","In-Hyderabad-1"
    )
    print(f"Updated port: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

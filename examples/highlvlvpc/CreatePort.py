from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # Reserve a floating IP via create_port (floating_ip=True)
    # POST /v1/highlvlvpc/create_port
    create_port_response = client.highlvlvpc.create_port(
        floating_ip=True,
        name="enter the port name",
        network_id="enter the network krn",
        subnet_id="enter the subnet krn",
        vpc_id="enter the vpc krn",
        x_region="enter the region name",
        # x_region possible values "In-Bangalore-1","In-Hyderabad-1"
    )
    print(f"Port created: {create_port_response}")
    print(f"port_krn={create_port_response.port_krn}")
    print(f"floating_ip={create_port_response.floating_ip_address}")

except Exception as e:
    print(f"Exception has occurred: {e}")

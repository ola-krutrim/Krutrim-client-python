from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # POST /kbs/v1/volumes/{volume_id}/action?op=attach
    resp = client.kbs.attach_volume(
        "enter the volume KRN",
        instance_id="enter the instance KRN",
        k_tenant_id="enter the VPC KRN",
        x_region="enter the region name",
        mount_partition="/dev/vdz",
        # x_region possible values "In-Bangalore-1","In-Hyderabad-1"
    )
    print(f"Attach result: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

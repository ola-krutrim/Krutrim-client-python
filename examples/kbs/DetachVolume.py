from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # POST /kbs/v1/volumes/{volume_id}/action?op=detach
    # attachment_id comes from volume.attachments[].remote_attachment_id (after attach completes)
    resp = client.kbs.detach_volume(
        "enter the volume KRN",
        instance_id="enter the instance KRN",
        attachment_id="enter the attachment id",
        k_tenant_id="enter the VPC KRN",
        x_region="enter the region name",
        # x_region possible values "In-Bangalore-1","In-Hyderabad-1"
    )
    print(f"Detach result: {resp}")

except Exception as e:
    print(f"Exception occurred: {e}")

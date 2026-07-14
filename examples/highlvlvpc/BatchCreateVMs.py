from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # POST /vm/v1/batch-vm-create → {batch_source, job_id, message, total_count}
    resp = client.highlvlvpc.batch_create_vms(
        template_krn="enter the template krn",
        count=2,
        instanceName="enter the instance name prefix",
        x_region="enter the region name",
        # x_region possible values "In-Bangalore-1","In-Hyderabad-1"
    )
    print(f"Batch create started: {resp}")
    print(f"job_id={resp.job_id}")

except Exception as e:
    print(f"Exception occurred: {e}")

from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # GET /vm/v1/instance-templates/details?template_krn=...
    template = client.highlvlvpc.retrieve_instance_template(
        template_krn="enter the template krn",
        x_region="enter the region name",
        # x_region possible values "In-Bangalore-1","In-Hyderabad-1"
    )
    print(f"Template details: {template}")

except Exception as e:
    print(f"Exception occurred: {e}")

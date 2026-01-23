import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)


try:
    get_templates = client.asg.v1.with_raw_response.get_launch_templates(
        vpc_id="Enter the VPC KRN ID",
        page=1,
        size=100,
        x_region="Enter the Region"
    )

    print(f"{get_templates.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")
import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)


try:
    delete_template = client.asg.v1.with_raw_response.delete_launch_template(
        template_id="Enter the Template ID",
        template_name="Enter the Template Name",
        version=1, #Select which version you want to delete
        x_region="Enter the Region"
    )

    print(f"{delete_template.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")
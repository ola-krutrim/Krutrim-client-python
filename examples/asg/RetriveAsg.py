import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)


try:
    retrive_asg = client.asg.v1.with_raw_response.retrieve_asg(
        asg_krn = "Enter the asg KRN ID",
        asg_name = "Enter the asg name",
        page=1,
        size=30,
        x_region="Enter the Region"
    )

    print(f"{retrive_asg.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")
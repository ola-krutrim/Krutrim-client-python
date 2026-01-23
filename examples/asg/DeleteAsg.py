import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)


try:
    delete_asg = client.asg.v1.with_raw_response.delete_asg(
        asg_krn = "Enter the asg KRN ID"
    )

    print(f"{delete_asg.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")
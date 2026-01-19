import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)


try:
    expiring_certs = client.certs.with_raw_response.get_expiring(
        date = "Enter the Date",
        vpc_id = "Enter the VPC ID"
    )

    print(f"{expiring_certs.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")
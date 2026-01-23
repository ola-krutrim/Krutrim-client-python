import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)


try:
    krn_by_vpc = client.asg.with_raw_response.get_asg_krn_by_vpc(
        page = 1,
        size = 100,
        vpc_krn = "Enter the vpc KRN ID"
    )

    print(f"{krn_by_vpc.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")
import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

# Load env
load_dotenv()
api_key = os.getenv("API_KEY")

# Init client
client = KrutrimClient(api_key=api_key)
try:
    resp = client.lb.with_raw_response.list_load_balancers_by_vpc(
        x_region="enter the x_region",
        vpc_krn="enter vpc krn"
    )
    print("Response:", resp.json())
except Exception as e:
    print(f"Error has occurred: {e}")
import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

# Load env
load_dotenv()
api_key = os.getenv("API_KEY")

# Init client
client = KrutrimClient(api_key=api_key)
try:
    resp = client.lb.with_raw_response.get_full_tg_list(
        vpc_id="enter vpc id",
        x_region="enter the x_region",
        # x_region possible values "In-Bangalore-1" 
    )
    print("Response:", resp.json())
except Exception as e:
    print(f"Error has occurred: {e}")

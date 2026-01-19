import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

# Load env
load_dotenv()
api_key = os.getenv("API_KEY")

# Init client
client = KrutrimClient(api_key=api_key)
try:
    resp = client.lb.with_raw_response.get_detailed_target_groups(
        x_region="enter the x_region",
        # x_region possible values "In-Bangalore-1"
        k_customer_id = "enter the k_customer_id",
        x_account_id = "enter the x_account_id",
        vpc_id="enter vpc id",
        target_group_name= "enter target group name"
    )
    print("Response:", resp.json())
except Exception as e:
    print(f"Error has occurred: {e}")
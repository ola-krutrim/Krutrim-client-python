from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")

client = KrutrimClient(api_key = api_key)


try:
    get_sshkey_response = client.sshkey.list_sshkeys(
        customer_id = "enter the customer id",
        x_region = "enter the region",
        page = 1,
        limit = 10,
        # x_region possible values "In-Bangalore-1","In-Hyderabad-1"
    )
    print(f"Successfully retrieved the SSH Key List {get_sshkey_response.json()}!")
except Exception as e:
    print(f"Exception! {e}")

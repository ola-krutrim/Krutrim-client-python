from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")

client = KrutrimClient(api_key=api_key)


try:
    # GET /v2/sshkeys/{customer_id}?sortBy=createdAt&sortOrder=desc&page=1&limit=10
    # Headers: k-customer-id, x-region, Accept: */*, Content-Type: application/json
    get_sshkey_response = client.sshkey.list_sshkeys(
        customer_id="enter the customer id",
        x_region="enter the region",
        # x_region possible values: "In-Bangalore-1", "In-Hyderabad-1"
        sort_by="createdAt",
        sort_order="desc",
        page=1,
        limit=10,
    )
    # Typed: .meta and .ssh_keys  |  204 / no keys → ssh_keys == []
    print(f"Successfully retrieved the SSH Key List {get_sshkey_response}!")
    print(f"total keys: {len(get_sshkey_response.ssh_keys)}")
    if get_sshkey_response.meta is not None:
        print(f"meta.total: {get_sshkey_response.meta.total}")
except Exception as e:
    print(f"Exception! {e}")

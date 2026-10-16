from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")

client = KrutrimClient(api_key = api_key)


try:
    response = client.sshkey.with_raw_response.create_sshkey(
        key_name="enter the key name",
        public_key="enter the rsa public key",
        x_region="enter the region",
        customer_id="enter the customer id",
    )

    print(f"Successfully Created {response.json()}")

except Exception as e:
    print("Error:", repr(e))
import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")

client = KrutrimClient(api_key=api_key)
 

try:
    resp = client.iam.list_policies(
        limit=999,
        offset=0,
        krutrim_managed="all"
    )

    print("Policies:", resp)

except Exception as e:
    print("Error:", repr(e))
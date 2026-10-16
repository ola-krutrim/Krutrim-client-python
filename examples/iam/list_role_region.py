import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")

client = KrutrimClient(api_key=api_key)
client.token = api_key  

try:
    resp = client.iam.list_roles(
        limit=999,
        offset=0,
        krutrimManaged=True,  # Optional: True, False, or "all" (default: "all")
    )

    print("Roles:", resp)

except Exception as e:
    print("Error:", repr(e))

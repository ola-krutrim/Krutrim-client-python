import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")

client = KrutrimClient(api_key=api_key)

try:
    resp = client.iam.delete_role(
        role_krn="enter the rolekrn",

    )

    print("Role Deleted:", resp)

except Exception as e:
    print("Error:", repr(e))
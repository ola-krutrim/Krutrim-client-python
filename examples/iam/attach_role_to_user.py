import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")

client = KrutrimClient(api_key=api_key)

try:
    resp = client.iam.assign_roles_to_user(
        user_id="enter the user_id",
        role_ids=[
        "enter the role_id",
        ],
        group_ids=[],  # optional

    )

    print("Roles Assigned to User:", resp)

except Exception as e:
    print("Error:", repr(e))



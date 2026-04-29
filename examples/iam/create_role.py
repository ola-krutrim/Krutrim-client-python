import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")

client = KrutrimClient(api_key=api_key)

try:
    resp = client.iam.create_role_with_policies(
        role_name="enter the role name",
        description="ente the role description",
        policy_ids=[
            "enter the policy_id",
        ],
    )

    print("Role Created with Policies:", resp)

except Exception as e:
    print("Error:", repr(e))
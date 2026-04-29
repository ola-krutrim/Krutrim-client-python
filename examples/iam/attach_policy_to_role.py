import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

# Load the API key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

# Create a client instance
client = KrutrimClient(api_key=api_key)

try:
    resp = client.iam.attach_policies_to_role(
        role_id="your-role-id-here",
        policy_ids=[
            "policy-id-1",
            "policy-id-2",
        ],
    )

    print("Policies Attached to Role:", resp)

except Exception as e:
    print("Error:", repr(e))
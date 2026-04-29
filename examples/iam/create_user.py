import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

# Load the API key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

# Create a client instance
client = KrutrimClient(api_key=api_key)

try:
    resp = client.iam.create_user(
        user_name="enter the user_name",
        email="enter the email",
        password="enter the password",
        console_access=True,
        
    )

    print("User Created:", resp)

except Exception as e:
    print("Error:", repr(e))

import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

# Load the API key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

# Create a client instance
client = KrutrimClient(api_key=api_key)

try:
    resp = client.iam.enable_programmatic_access(
        user_krn="enter the userkrn",
    )

    print("Programmatic Access Enabled:", resp)

except Exception as e:
    print("Error:", repr(e))

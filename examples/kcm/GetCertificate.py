import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)


try:
    
    certificate = client.certs.with_raw_response.retrieve(
        cert_id = "Enter the Certificate Id"
    )

    
    print(f"{certificate.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")
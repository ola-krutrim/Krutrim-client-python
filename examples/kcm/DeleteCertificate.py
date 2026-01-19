import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)


try:

    delete_cert_response = client.certs.with_raw_response.delete(
        path_cert_id = "Enter the certificate ID"
    )
    if delete_cert_response.status_code == 204:
        print("Certificate deleted successfully")
    else:
        print(f"Unexpected status code: {delete_cert_response.status_code}")
        print(f"{delete_cert_response.json()}")


except Exception as e:
    print(f"Error has occurred: {e}")
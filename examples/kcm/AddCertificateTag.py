
import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)


try:

    add_certificate_tag_response = client.certs.tags.with_raw_response.addCertificateTag(
    path_cert_id = "Enter Certificate ID",
    tags = {
        "Enter Tag Name": "Enter Tag Value"
    }
    )

    
    print(f"{add_certificate_tag_response.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")
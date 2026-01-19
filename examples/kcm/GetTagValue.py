import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)


try:
    
    get_tag_value = client.tags.with_raw_response.getTagValue(
        cert_id = "Enter the Certificate ID",
        tag_name = "Enter the Tag Name"
    )

    
    print(f"{get_tag_value.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")
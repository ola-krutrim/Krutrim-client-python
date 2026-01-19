from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    fetch_record = client.v1.record.with_raw_response.fetchrecord(
        zoneid="enter zone_id",
    )

    print(f"Successfully fetched the record: {fetch_record.json()}")

except Exception as e:
    print(f"Exception: {e}")

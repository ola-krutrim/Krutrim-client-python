from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    fetch_zone_by_id = client.v1.zone.with_raw_response.fetchZoneById(
        zoneid = "Enter the zone id"
    )

    print(f"Successfully fetched the zone by Id: {fetch_zone_by_id.json()}")

except Exception as e:
    print(f"Exception: {e}")

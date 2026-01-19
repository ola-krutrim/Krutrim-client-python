from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    fetch_zone = client.v1.zone.with_raw_response.fetch()

    print(f"Successfully fetched the zone: {fetch_zone.json()}")

except Exception as e:
    print(f"Exception: {e}")

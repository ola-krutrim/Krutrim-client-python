from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    remove_zone = client.v1.zone.delete(
        zoneid="enter zone_id" 
    )

    print(f"Successfully removed the zone")

except Exception as e:
    print(f"Exception: {e}")

from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    add_zone = client.v1.zone.with_raw_response.create(
        zonename="enter the zone_name",
        type="enter the type", #private
        vpcid="enter the vpc_id",
        subnetid="enter the subnet_id"   
    )

    print(f"Successfully added the zone{add_zone.json()}")

except Exception as e:
    print(f"Exception: {e}")

from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    add_vpc = client.v1.zone.vpc.with_raw_response.add(
        vpcinfo=["krn:vpc:In-Bangalore-1:0259427492:92945705-e555-4666-a253-d7ccd47c6107:vpc:eda7c905-de43-435c-8ac3-e9ce80b76224"],
        zoneid="krn:pdns:In-Bangalore-1:0259427492:92945705-e555-4666-a253-d7ccd47c6107:pdns_zone:75516d66-bfbd-470e-8921-b15b7af8434d"  
    )

    print(f"Successfully added the zone: {add_vpc.json()}")

except Exception as e:
    print(f"Exception: {e}")

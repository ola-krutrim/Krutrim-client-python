from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    update_record = client.v1.record.update(
        rname="enter the record name",
        value="enter the value",  #10.10.10.123
        TYPE="A", #enter as per requirement
        routing="enter routing type", #example: "SIMPLE"
        recordid="entet the record_id",
    )

    print(f"Successfully updated the record: {update_record}")

except Exception as e:
    print(f"Exception: {e}")

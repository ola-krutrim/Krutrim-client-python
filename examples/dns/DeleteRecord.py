from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    delete_record = client.v1.record.delete(
        recordid="enter record_id"
    )

    print(f"Successfully deleted the record")

except Exception as e:
    print(f"Exception: {e}")

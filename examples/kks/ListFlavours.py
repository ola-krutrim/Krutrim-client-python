from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    list_flavours = client.kks.with_raw_response.list_flavors()

    print(f"Successfully Listed all Flavours {list_flavours.json()}")

except Exception as e:
    print(f"Exception: {e}")
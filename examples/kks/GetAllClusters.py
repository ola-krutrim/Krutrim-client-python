from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    get_clusters = client.kks.clusters.with_raw_response.list()

    print(f"Successfully fetched all the clusters {get_clusters.json()}")

except Exception as e:
    print(f"Exception: {e}")

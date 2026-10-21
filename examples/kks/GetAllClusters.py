import os

from dotenv import load_dotenv

from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    get_clusters = client.kks.clusters.with_raw_response.list(region="In-Bangalore-1")

    print(f"Successfully fetched clusters in In-Bangalore-1 {get_clusters.json()}")

except Exception as e:
    print(f"Exception: {e}")

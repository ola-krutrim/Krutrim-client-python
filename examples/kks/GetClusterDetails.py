from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    get_cluster_details = client.kks.clusters.with_raw_response.retrieve(
        cluster_krn = "enter the cluster krn",
    )

    print(f"Successfully fetched the cluster details {get_cluster_details.json()}")

except Exception as e:
    print(f"Exception: {e}")

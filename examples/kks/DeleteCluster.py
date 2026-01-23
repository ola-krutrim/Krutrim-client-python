from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    delete_cluster = client.kks.clusters.with_raw_response.delete(
        cluster_krn = "enter the cluster krn",
    )

    print(f"Successfully deleted the cluster {delete_cluster.json()}")

except Exception as e:
    print(f"Exception: {e}")

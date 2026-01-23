from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    list_cluster_addons = client.kks.clusters.addons.with_raw_response.list(
        cluster_krn = "enter the cluster krn"
    )

    print(f"Successfully fetched all the cluster addons {list_cluster_addons.json()}")

except Exception as e:
    print(f"Exception: {e}")

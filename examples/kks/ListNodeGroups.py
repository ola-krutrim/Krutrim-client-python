from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    list_node_groups = client.kks.clusters.node_groups.with_raw_response.list(
        cluster_krn = "enter the cluster krn "
    )

    print(f"Successfully fetched all the node groups {list_node_groups.json()}")

except Exception as e:
    print(f"Exception: {e}")

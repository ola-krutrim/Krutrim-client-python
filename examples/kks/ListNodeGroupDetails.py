from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    get_nodegroup_details = client.kks.clusters.node_groups.with_raw_response.retrieve(
        cluster_krn = "enter the cluster krn",
        nodegroup_krn = "enter the node group krn"
    )

    print(f"Successfully fetched the node group details {get_nodegroup_details.json()}")

except Exception as e:
    print(f"Exception: {e}")

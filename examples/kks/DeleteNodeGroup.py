from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    delete_node_group = client.kks.clusters.node_groups.with_raw_response.delete(
        cluster_krn = "enter the cluster krn",
        nodegroup_krn = "enter the node group krn",
    )

    print(f"Successfully deleted the node group" )

except Exception as e:
    print(f"Exception: {e}")

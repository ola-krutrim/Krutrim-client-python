from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    update_node_group_config = client.kks.clusters.node_groups.with_raw_response.update_config(
        nodegroup_krn = "enter the nodegroup krn",
        cluster_krn = "enter the cluster krn",
        scaling_config = {"min_size": 2, "max_size": 5, "desired_size": 4},
    )

    print(f"Successfully updated the nodegroup config {update_node_group_config.json()}")

except Exception as e:
    print(f"Exception: {e}")

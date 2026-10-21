import os

from krutrim_client import KrutrimClient

with KrutrimClient(region="In-Hyderabad-2") as client:
    result = client.kks.clusters.node_groups.update_config(
        nodegroup_krn=os.environ["NODEGROUP_KRN"],
        cluster_krn=os.environ["CLUSTER_KRN"],
        scaling_config={"min_size": 2, "max_size": 5, "desired_size": 4},
    )
    print(result)

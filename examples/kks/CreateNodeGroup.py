from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

cluster_krn = "enter the cluster krn"


try:
    create_node_group = client.kks.clusters.node_groups.with_raw_response.create(
        cluster_krn=cluster_krn,
        name="enter the name",
        instance_types="enter the flavor",
        disk_size=100,                                  #update disk size as per requirement
        subnets_krn="enter the krn",
        scaling_config={
            "minSize":1,                               #modify as per requirement
            "maxSize":5,
            "desiredSize":2,

        },
        remote_access={
            "sshKeyKrn":"enter the sshkeykrn",
            "source_security_groups_krns":[]
        },
        node_repair_config={
            "enabled":True
        },  
        labels={},
        taints= []

    )

    print("Successfully created node group")
    print(create_node_group.json())

except Exception as e:
    print(f"Exception: {e}")

        # labels={
        #     "environment": "production",
        #     "team": "backend"
        # },
        # {
        #     "key": "dedicated",
        #     "value": "gpu",
        #     "effect": "NoSchedule"
        # }



# {
#     "nodegroup": {
#         "name": "default-pool",
#         "krn": "krn:kks::6419347276:df18aa35-b845-4e61-b739-32a3a4e219d3:nodegroup:673c5749-2f98-45ef-bb1d-6aacb8a7c682",
#         "clusterKrn": "krn:kks:In-Bangalore-1:6419347276:df18aa35-b845-4e61-b739-32a3a4e219d3:cluster:639d2b89-ed93-4951-b1e3-ba0ad4ae110b",
#         "createdAt": 1769083300.062727,
#         "updatedAt": 1769083300.062727,
#         "userUpdatedAt": 1769083300.0621705,
#         "instanceTypes": "CPU-4x-16GB",
#         "labels": {
#             "environment": "productiion"
#         },
#         "remoteAccess": {
#             "sshKeyKrn": "krn:krutrim-ssh:In-Bangalore-1:6419347276:df18aa35-b845-4e61-b739-32a3a4e219d3:sshkey:37876055-60b9-4ce0-b129-157242caad31",
#             "sourceSecurityGroupsKrns": [
#                 "krn:krutrim-sg:In-Bangalore-1:6419347276:df18aa35-b845-4e61-b739-32a3a4e219d3:sg:5fe3fce9-e690-4b5c-97dc-07edabc5f362"
#             ]
#         },
#         "scalingConfig": {
#             "desiredSize": 2,
#             "maxSize": 5,
#             "minSize": 1
#         },
#         "subnetsKrn": "krn:vpc:In-Bangalore-1:6419347276:df18aa35-b845-4e61-b739-32a3a4e219d3:subnet:e74d5566-9e03-4854-b578-0ab5f0c87113",
#         "taints": [
#             {
#                 "effect": "NoSchedule",
#                 "key": "dedicated",
#                 "value": "gpu"
#             }
#         ],
#         "diskSize": 100,
#         "status": "CREATING",
#         "version": "1.34"
#     }
# }
# # try:
# #     create_node_group = client.kks.clusters.node_groups.with_raw_response.create(
# #         cluster_krn=cluster_krn,
# #         name="default-pool34",
# #         instance_types="CPU-4x-16GB",
# #         disk_size=100,
# #         subnets_krn="krn:vpc:In-Bangalore-1:7344783839:2fbf2544-0c1d-481c-b745-4ef99e564b41:subnet:00d775d5-8b39-4980-ad8b-eb96374cb6f7",
# #         scaling_config={
# #             "minSize":1,
# #             "maxSize":5,
# #             "desiredSize":2,
# #         },
# #         remote_access={
# #             "source_security_groups_krns":[]
# #         },
# #         node_repair_config={
# #             "enabled":True
# #         },
# #     )

# #     print("Successfully created node group")
# #     print(create_node_group.json())

# # except Exception as e:
# #     print(f"Exception: {e}")
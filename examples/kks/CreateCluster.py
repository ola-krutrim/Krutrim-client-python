from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    create_cluster = client.kks.clusters.with_raw_response.create(
        vpcKrn = "enter the vpc krn",
        subnetKrns = "enter the subnetkrn",
        podIpv4Cidr = "enter the cidr",
        serviceIpv4Cidr = "enter the cidr",
        name ="enter the name",
        version = "enter the version",
    )

    print(f"Successfully created the cluster {create_cluster.json()}")

except Exception as e:
    print(f"Exception: {e}")



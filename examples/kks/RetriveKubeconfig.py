from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    retrive_kubeconfig = client.kks.clusters.with_raw_response.retrieve_kubeconfig(
        cluster_krn = "krn:kks:In-Bangalore-1:6419347276:df18aa35-b845-4e61-b739-32a3a4e219d3:cluster:0951ed93-9e4d-48a7-871e-31837577c41d"
    )

    print(f"Successfully Retrived Kubeconfig {retrive_kubeconfig.text()}")

except Exception as e:
    print(f"Exception: {e}")
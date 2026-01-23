from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    delete_addon = client.kks.clusters.addons.delete(
        cluster_krn = "enter the cluster krn",
        addon_krn = "enter the addon krn",

    )

    print(f"Successfully deleted the addon")

except Exception as e:
    print(f"Exception: {e}")

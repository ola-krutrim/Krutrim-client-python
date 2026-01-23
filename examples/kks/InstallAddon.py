from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    install_addons = client.kks.clusters.with_raw_response.addons.install(
        addon_name = "enter the addon name",
        cluster_krn = "enter the cluster krn"

    )

    print(f"Successfully installed the addon {install_addons.json()}")

except Exception as e:
    print(f"Exception: {e}")

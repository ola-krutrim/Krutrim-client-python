
import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)


try:
    upscale_asg = client.asg.v1.with_raw_response.upscale_asg(
        asg_krn = "Enter the asg KRN ID",
        desired_vm_count = 3,          #Enter the desired VM count
        vpc_krn = "Etner the VPC KRN ID"
    )

    print(f"{upscale_asg.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")



from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    create_vm_response = client.highlvlvpc.create_instance(
        image_krn="enter the image krn",
        instanceName="enter the name",
        instanceType="enter the instance type",
        network_id="enter the network krn",
        subnet_id="enter the subnet krn",
        vpc_id="enter the vpc krn",
        region="enter the region",
        sshkey_name="enter the ssh key name",
        security_groups=["enter the security group krn"],
        floating_ip=True,   
        volume_name="enter the volume name",
        volume_size=20,                                                #enter as per requirement
        volumetype="enter the volume type",
        user_data="",
        delete_on_termination=True,
        port_krn="",
        isGpu=False,
        volumes=[],
        tags=[],
        timeout=6000,
    )

    print(f"Created VM successfully: {create_vm_response}")

except Exception as e:
    if "504" in str(e):
        print("VM creation request likely succeeded but timed out. Please check UI or use list API.")
    else:
        print(f"Exception occurred: {e}")


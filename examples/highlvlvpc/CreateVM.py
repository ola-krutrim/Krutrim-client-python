from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # Option A: attach an existing volume (omit image_krn, volume_name, volume_size, volumetype)
    create_vm_response = client.highlvlvpc.create_instance(
        instanceName="enter the name",
        instanceType="enter the type",
        subnet_id="enter the subnetid",
        vpc_id="enter the vpcid",
        region="enter the region",
        sshkey_name="enter the sshkey name",
        security_groups=["enter the security group name"],
        floating_ip=True,
        user_data="",
        delete_on_termination=True,
        port_krn="",
        isGpu=False,
        volumes=["enter the volume krn"],
        tags=[],
        timeout=6000,
    )

    # Option B: create a new boot volume (omit volumes, provide image_krn + volume fields)
    # create_vm_response = client.highlvlvpc.create_instance(
    #     image_krn="krn:kbs:In-Bangalore-1:4144076351:...:image:...",
    #     instanceName="moni",
    #     instanceType="CPU-4x-16GB",
    #     subnet_id="...",
    #     vpc_id="...",
    #     region="In-Bangalore-1",
    #     sshkey_name="jawakey",
    #     security_groups=["..."],
    #     floating_ip=True,
    #     volume_name="moni-boot-volume",
    #     volume_size=40,
    #     volumetype="SSD",
    #     timeout=6000,
    # )

    print(f"Created VM successfully: {create_vm_response}")

except Exception as e:
    if "504" in str(e):
        print("VM creation request likely succeeded but timed out. Please check UI or use list API.")
    else:
        print(f"Exception occurred: {e}")


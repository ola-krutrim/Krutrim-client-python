from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # Option A: attach an existing volume
    # POST /vm/v1/create_instance_async → {message, task_id}
    # Omit image_krn, volume_name, volume_size, volumetype when volumes is set.
    create_vm_response = client.highlvlvpc.create_instance(
        instanceName="enter the name",
        instanceType="Enter the instance type",
        subnet_id="Enter the subnet ID",
        vpc_id="Enter the VPC ID",
        region="enter the region",
        sshkey_name="enter the ssh key name",
        security_groups=["enter the security group name"],
        floating_ip=True,
        user_data="",
        volumes=["enter the volume krn"],
        tags=[],
        delete_on_termination=True,
        count=1,
        port_krn="",
        isGpu=False,
        timeout=6000,
    )

    # Option B: create a new boot volume from image (omit volumes)
    # create_vm_response = client.highlvlvpc.create_instance(
    #     image_krn="enter the image krn",
    #     instanceName="enter the instance name",
    #     instanceType="enter the instance type",
    #     subnet_id="enter the subnet ID",
    #     vpc_id="enter the VPC ID",
    #     region="enter the region",
    #     sshkey_name="enter the ssh key name",
    #     security_groups=["enter the security group name"],
    #     floating_ip=True,
    #     volume_name="enter the volume name",
    #     volume_size=20,
    #     volumetype="enter the volume type",
    #     delete_on_termination=True,
    #     user_data="",
    #     tags=[],
    #     count=1,
    #     timeout=6000,
    # )

    print(f"Instance creation started: {create_vm_response}")
    print(f"task_id={create_vm_response.task_id}")

except Exception as e:
    print(f"Exception occurred: {e}")

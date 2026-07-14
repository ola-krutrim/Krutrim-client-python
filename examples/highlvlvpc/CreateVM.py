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
    #     image_krn="krn:vm:In-Bangalore-1:default:default:image:498a1efb-4ca4-482b-bb5c-a51660f94215",
    #     instanceName="test",
    #     instanceType="CPU-2x-8GB",
    #     subnet_id="krn:vpc:In-Bangalore-1:9639998375:619a13ac-18ce-4728-8d44-8bc81e6b0704:subnet:e92524ac-d7e4-4b73-b2da-31a78cb28318",
    #     vpc_id="krn:vpc:In-Bangalore-1:9639998375:619a13ac-18ce-4728-8d44-8bc81e6b0704:vpc:d8c33bbf-484b-432b-8698-78709418e1e7",
    #     region="In-Bangalore-1",
    #     sshkey_name="ksm-phase-1",
    #     security_groups=["krn:krutrim-sg:In-Bangalore-1:9639998375:619a13ac-18ce-4728-8d44-8bc81e6b0704:sg:03da368c-6c68-4bfb-9d18-464b6beb6d1f"],
    #     floating_ip=True,
    #     volume_name="test-4751d8-a82c3",
    #     volume_size=20,
    #     volumetype="HNSS",
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

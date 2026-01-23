import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient
from krutrim_client.types.asg import VolumeParam
from krutrim_client.types.asg import PolicyParam


load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    create_template = client.asg.v1.with_raw_response.create_launch_template(
        vpc_krn="Enter the VPC KRN ID",
        instance_name="Enter the instance name",
        instance_type="Enter the instance type",
        region="Enter the region",
        security_groups=[
            "Enter the Security Group Krn ID 1",
            "Enter the security group KRN ID 2 and so on",
        ],
        sshkey_name="Enter the ssh key name",
        user_data="Enter an executable boot time command ex: #!bash sdk.sh",
        volume_name="Enter the Volume Name",
        image_krn="Enter the Image KRN ID",
        vpc_name="Enter the VPC name",
        subnet_id="Enter the Subnet ID",
        template_name="Enter the Template name",
        volume_size=[
            VolumeParam(
                count=1,         #Enter the Volume Count
                volume_size=20,  #Enter the Volume Size
            ),
            VolumeParam(
                count=1,
                volume_size=20,
            ),
            # and add so on for multiple volumes selection
        ],

        policy=[
            PolicyParam(
                predefined_metric_specification={
                    "PredefinedMetricType": "AverageCPUUtilization"
                },
                up_scale_target_value=70,     #Enter the up scale target value
                down_scale_target_value=40,   #Enter the down scale target value
                scale_out_cooldown=10,        #Enter the scale out cooldown time in sec
                scale_in_cooldown=10,         #Enter the scale in cooldown time in sec
            ),

            # Scheduled
            PolicyParam(
                predefined_metric_type="PutScheduledAction",
                up_scale_time="Enter the upscale schedule time in format 07:00:00.000000",
                down_scale_time="Enter the downscale schedule time in format 22:00:00.000000",
            )
        ],
        volume_type="Enter the Volume Type",
        min=2,   #Enter the minimum instance count
        max=6,   #Enter the maximum instance count
    )
    print(create_template.json())

except Exception as e:
    print(f"Error has occurred: {e}")


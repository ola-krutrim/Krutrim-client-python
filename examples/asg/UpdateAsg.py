import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient
from krutrim_client.types.asg import VolumeParam
from krutrim_client.types.asg import PolicyParam


load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:

   update_asg_response = client.asg.v1.with_raw_response.update_asg(
        # -------- REQUIRED --------
        asg_krn="Enter the asg KRN ID",
        # -------- INSTANCE --------
        instance_type="Enter the instance type",
        # -------- VOLUME --------
        volume_name = "Enter the Volume Name",
        volume_size=[
            VolumeParam(
                count=1,       #Enter the Volume Count
                volume_size=4, #Enter the Volume Size
            ),
            VolumeParam(        
                count=1,       
                volume_size=4,
            ),
            # and add so on for multiple volumes selection
        ],

        # -------- ASG --------
        min=2, #Enter the minimum instance count
        max=5, #Enter the maximum instance count
        # -------- POLICY --------
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

        # -------- ssh_key --------
        sshkey_name="Enter the ssh key name",

        # -------- ssh_key --------
        security_groups=[
            "Enter the Security Group Krn ID 1",
            "Enter the security group KRN ID 2 and so on",
        ],

        # -------- METADATA --------
        user_data = "Enter an executable boot time command ex: #!bash sdk.sh"
    )

   print(update_asg_response.json())

except Exception as e:
    print(f"Error has occurred: {e}")


    
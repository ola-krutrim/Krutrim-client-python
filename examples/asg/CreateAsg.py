import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient
from krutrim_client.types.asg import VolumeParam
from krutrim_client.types.asg import PolicyParam


load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    create_asg_response = client.asg.v1.with_raw_response.create_asg(
        # -------- HEADER --------
        x_region="Enter the region",

        # -------- CORE --------
        vpc_krn="Enter the VPC KRN ID",
        region="Enter the region",
        asg_name="Enter the asg name",
        vpc_name="Enter the vpc name",

        # -------- INSTANCE --------
        instance_name="Enter the instance name",
        instance_type="Enter the instance type",

        # -------- IMAGE --------
        image_krn="Enter the Image KRN ID",

        # -------- NETWORK --------
        subnet_id="Enter the Subnet ID",

        # -------- SECURITY --------
        sshkey_name="Enter the ssh key name",
        security_groups=[
            "Enter the Security Group Krn ID 1",
            "Enter the security group KRN ID 2 and so on",
        ],

        # -------- VOLUMES --------
        volume_name="Enter the Volume Name",
        volume_type="Enter the Volume Type",
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
        launch_from_template=False,
        launch_template_id = "Enter the template Id",
        launch_template_version = 1,  #Enter the version number of template
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

        # -------- TEMPLATE --------
        save_as_template=False,  #True or false on basis of you want to save this as template or not

        # -------- TAGS --------
        user_data = "Enter an executable boot time command ex: #!bash sdk.sh"  
    )

    print(create_asg_response.json())

except Exception as e:
    print(f"Error has occurred: {e}")


    
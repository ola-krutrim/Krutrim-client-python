import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient
from krutrim_client.types.asg import VolumeParam
from krutrim_client.types.asg import PolicyParam


load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:

     update_template = client.asg.v1.with_raw_response.update_launch_template(
        template_id="8eea5e0e-f843-11f0-b963-6e89ceb8bb39",
        template_name="templ345w54",

        instance_name="templ5644",
        instance_type="CPU-2x-8GB",
        sshkey_name="jawakey",
        # user_data="Enter an executable boot time command ex: #!bash sdk.sh",

        image_krn="krn:vm:In-Bangalore-1:default:default:image:498a1efb-4ca4-482b-bb5c-a51660f94215",

        security_groups=[
            "krn:sg:In-Bangalore-1:6419347276:df18aa35-b845-4e61-b739-32a3a4e219d3:sg:12345678-1234-1234-1234-123456789012",
            # "Enter the security group KRN ID 2 and so on",
        ],

        min=4,   #Enter the minimum instance count
        max=6,   #Enter the maximum instance count
        volume_name="vol09i8u23",
        volume_type="HNSS",
        volume_size=[
            VolumeParam(
                count=1,         #Enter the Volume Count
                volume_size=28,  #Enter the Volume Size
            ),
            # VolumeParam(
            #     count=1,
            #     volume_size=20,
            # ),
            # and add so on for multiple volumes selection
        ],

        policy=[
            PolicyParam(
                predefined_metric_specification={
                    "PredefinedMetricType": "AverageCPUUtilization"
                },
                up_scale_target_value=90,     #Enter the up scale target value
                down_scale_target_value=20,   #Enter the down scale target value
                scale_out_cooldown=10,        #Enter the scale out cooldown time in sec
                scale_in_cooldown=10,         #Enter the scale in cooldown time in sec
            ),

            # Scheduled
            PolicyParam(
                predefined_metric_type="PutScheduledAction",
                up_scale_time="06:00:00.000000",
                down_scale_time="10:00:00.000000",
            )
        ],
     )



     print(f"Template updated successfully : {update_template.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")
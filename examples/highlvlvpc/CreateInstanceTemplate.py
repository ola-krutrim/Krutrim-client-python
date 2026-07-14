from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
client = KrutrimClient(api_key=api_key)

try:
    # POST /vm/v1/instance-templates/create
    template = client.highlvlvpc.create_instance_template(
        name="enter the template name",
        volume_name="enter the volume name",
        vpc_id="enter the vpc krn",
        subnet_id="enter the subnet krn",
        instanceType="CPU-2x-8GB",
        isGpu=False,
        sshkey_name="enter the ssh key name",
        region="enter the region name",
        # region possible values "In-Bangalore-1","In-Hyderabad-1"
        image_krn="enter the image krn",
        volumetype="HNSS",
        volume_size=20,
        security_groups=["enter the security group krn"],
        user_data="",
    )
    print(f"Created template: {template}")
    print(f"template_krn={template.template_krn}")

except Exception as e:
    print(f"Exception occurred: {e}")

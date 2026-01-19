import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)


try:
    certificate_list = client.certs.with_raw_response.list(
        vpc_id = "Enter the VPC ID"
    )

    print(f"{certificate_list.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")





    #  vpc_id = "krn:vm:colo-1:1330618268:64151bfb-efcc-4c55-914e-1e497c7fb602:instance:ca633d8f-c370-49d7-88d5-c7e9fecc4760"
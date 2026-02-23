import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

# Load env
load_dotenv()
api_key = os.getenv("API_KEY")

# Init client
client = KrutrimClient(api_key=api_key)
try:
    resp = client.lb.with_raw_response.update_target_group(
        x_region="enter the region",  
        
        target_group_name="enter the target groupname", 
        
        k_customer_id="enter the kcustomerid",  
        
        x_account_id="enter the xaccountid",  
        
        vpc_id="enter the vpcid",
        
        
        members=[],
        
        health_monitor={}
    )

    print("Response:", resp.json())

except Exception as e:
    print(f"Error has occurred: {e}")




            # {
            # "name": "member_test_celery_1_10",
            # "address": "10.230.166.233",
            # "protocol_port": 3000,
            # "weight": 1
            # },
            # {
            # "name": "member_test_celery_2_10",
            # "address": "10.0.4.175",
            # "protocol_port": 5000,
            # "weight": 1
            # }



        # "h_type": "HTTP",
        # "timeout": 10,
        # "delay": 13,
        # "name": "LB-fullaccess-HM",
        # "url_path": "/",
        # "max_retries": 2
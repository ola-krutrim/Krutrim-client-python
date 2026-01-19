import os
from dotenv import load_dotenv
import  traceback
from krutrim_client import KrutrimClient

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    resp = client.lb.create_load_balancer_orchestration(
        k_customer_id="enter customer id",
        x_account_id="enter account id",
        x_region="enter x_region",
         # x_region possible values "In-Bangalore-1"  

        listeners=[],


        loadbalancer_data={},
        extra_body={"security_groups": []},
    )
    
    print("Successfully created LB Orchestration:", resp)

except Exception as e:
    print("Error has occurred:", repr(e))

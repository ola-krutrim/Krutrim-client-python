import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

# Load env
load_dotenv()
api_key = os.getenv("API_KEY")

# Init client
client = KrutrimClient(api_key=api_key)

try:
    create_tg_resp = client.lb.create_target_group(
        target_group_name="enter-your-target-group-name",
        vpc_id="enter vpc_krn",

        x_region="enter the region",
        # x_region possible values "In-Bangalore-1" 


        # Health monitor (API expects: type, delay, timeout, name)
        health_monitor={},

        # Backend members (API expects: name, address, protocol_port)
        members=[]
    )

    print(f"Successfully created Target Group: {create_tg_resp}")

except Exception as e:
    print(f"Error has occurred: {e}")


# examples of health monitor and members:

            # "name": "tg-hm-1",
            # "h_type": "HTTP",      # MUST be TCP / UDP / HTTP
            # "timeout": 5,
            # "delay": 10   



            # {
            #     "name": "member-1",
            #     "address": "10.0.4.175",
            #     "protocol_port": 5000,
            #     "weight": 1
            # },
            # {
            #     "name": "member-2",
            #     "address": "10.0.4.190",
            #     "protocol_port": 5000,
            #     "weight": 1
            # }
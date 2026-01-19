# python
import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient 

load_dotenv()
api_key = os.getenv("API_KEY")

client = KrutrimClient(api_key=api_key)

try:
    lb_krn="enter the load balancer krn"
    resp = client.lb.with_raw_response.update_load_balancer(

        path_lb_krn=lb_krn,
        x_region="enter the x_region",
        # x_region possible values "In-Bangalore-1"
        k_customer_id="enter the k_customer_id",
        x_account_id="enter the x_account_id",
        listeners=[],
        loadbalancer_data={

        },
        security_groups=[],
    )
    print(resp.status_code, resp.text)
except Exception as e:
    print(f"Error has occurred: {e}")



            # {
            #     "listener_data": {
            #         "listener_id": "6193a5b8-c25a-4979-948b-c7176bf4a343",
            #         "listener_index": 1,
            #         "listener_name": "web-listener",
            #         "protocol": "HTTP",
            #         "protocol_port": 80,
            #     },
            #     "policy_data": [
            #         {
            #             "action": "REDIRECT_TO_POOL",
            #             "policy_id": "6a588b1f-3b81-40fa-b7be-63a090e1f75a",
            #             "policy_name": "test-lb-1-policy-1",
            #             "rule_data": [
            #                 {
            #                     "compare_type": "STARTS_WITH",
            #                     "key": "",
            #                     "rule_id": "c1f3cc38-4258-43e3-9a1f-035666390fbc",
            #                     "rule_krn": "krn:loadbalancer-service:In-Bangalore-1:7344783839:2fbf2544-0c1d-481c-b745-4ef99e564b41:rule:72797759-8b8a-4b03-b2ec-bd1799999e62",
            #                     "type": "PATH",
            #                     "value": "/",
            #                 }
            #             ],
            #         }
            #     ],
            #     "pool_data": [
            #         {
            #             "admin_state_up": True,
            #             "healthmonitor_data": {
            #                 "delay": 10,
            #                 "h_type": "HTTP",
            #                 "health_monitor_id": "6bd47474-a10b-457f-a682-3da894c41ee4",
            #                 "max_retries": 3,
            #                 "name": "tg_testing_15th_oct",
            #                 "timeout": 5,
            #                 "url_path": "/",
            #             },
            #             "lb_algorithm": "ROUND_ROBIN",
            #             "member_data": [
            #                 {
            #                     "krn": "krn:loadbalancer-service:In-Bangalore-1:7344783839:2fbf2544-0c1d-481c-b745-4ef99e564b41:member:1f4d2055-559c-4e22-836c-82aba5113996",
            #                     "member_id": "2ce57b22-ef8b-4ca7-b1af-b32e2a753206",
            #                     "member_index": 1,
            #                     "status": "success",
            #                 },
            #                 {
            #                     "krn": "krn:loadbalancer-service:In-Bangalore-1:7344783839:2fbf2544-0c1d-481c-b745-4ef99e564b41:member:90bce6ed-f757-4c15-8e31-5b8f08fb7d57",
            #                     "member_id": "a512e1f9-5382-49f3-b35e-43d824d54135",
            #                     "member_index": 2,
            #                     "status": "success",
            #                 },
            #             ],
            #             "pool_id": "0c0b62ad-084d-4f1f-b3ce-8763229208e0",
            #             "pool_name": "test-lb-1-pool-1",
            #             "protocol": "HTTP",
            #             "target_group_name": "lb_apr_22_release_testing_TG",
            #         }
            #     ],
            # }



            # "create_port": True,
            # "description": "",
            # "floating_ip": False,
            # "lb_name": "test-lb-1",
            # "network_id": "krn:vpc:In-Bangalore-1:7344783839:2fbf2544-0c1d-481c-b745-4ef99e564b41:network:aea55436-84b9-4d08-87d1-8cc831ed2811",
            # "vip_subnet_id": "krn:vpc:In-Bangalore-1:7344783839:2fbf2544-0c1d-481c-b745-4ef99e564b41:subnet:15aaac4e-fc29-4c26-8283-d5ed1824ba85",
            # "vpc_id": "krn:vpc:In-Bangalore-1:7344783839:2fbf2544-0c1d-481c-b745-4ef99e564b41:vpc:0f716d62-fe5d-4aff-b23e-a277192b3546",            
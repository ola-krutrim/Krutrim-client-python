import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

# Load env
load_dotenv()
api_key = os.getenv("API_KEY")

# Init client
client = KrutrimClient(api_key=api_key)

try:

    update_cert_response = client.tags.with_raw_response.updateCertificate(

        path_cert_id = "Enter the Certificate ID",
        cert_file = "Enter the Certificate File Path",

        # form fields
        flag="0",    # use "0" or "1" as required

        # headers

        vpc_id="Enter the VPC ID",
    )

    print(f"{update_cert_response.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")




# try:

#     import_cert_resp = client.tags.with_raw_response.updateCertificate(

#         path_cert_id = "krn:kcm:colo-1:1330618268:64151bfb-efcc-4c55-914e-1e497c7fb602:certs:72aa120f-528e-40ac-bb93-0879be212d16",
#         cert_file = "/Users/bhanu.singh3/Documents/DEV/krutrim-client-sdk/bundle.p12",

#         # form fields
#         flag="0",    # use "0" or "1" as required

#         # headers

#         vpc_id="krn:vpc:colo-1:1330618268:64151bfb-efcc-4c55-914e-1e497c7fb602:vpc:8334f527-38e2-48d2-a7b5-a680bea0ca9a",
#     )

#     print(f"{import_cert_resp.json()}")

# except Exception as e:
#     print(f"Error has occurred: {e}")





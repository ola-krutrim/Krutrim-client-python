import os
from dotenv import load_dotenv
from krutrim_client import KrutrimClient

# Load env
load_dotenv()
api_key = os.getenv("API_KEY")

# Init client
client = KrutrimClient(api_key=api_key)

try:

    import_cert_resp = client.certs.with_raw_response.import_file(
        cert_file="enter the path to your certificate file here",

        # form fields
        name="enter the name",
        tags="{}",   # keep "{}" if API expects JSON-like tags
        flag="0",    # use "0" or "1" as required

        # headers

        vpc_id="enter the vpc id here",
    )

    print(f"{import_cert_resp.json()}")

except Exception as e:
    print(f"Error has occurred: {e}")




# try:

#     import_cert_resp = client.certs.with_raw_response.import_file(
#         cert_file="/Users/monissa.n1/Documents/SDK/krutrim-client-sdk/bundle.p12",

#         # form fields
#         name="certificate-name567564556556",
#         tags="{}",   # keep "{}" if API expects JSON-like tags
#         flag="0",    # use "0" or "1" as required

#         # headers

#         vpc_id="krn:vpc:colo-1:1330618268:64151bfb-efcc-4c55-914e-1e497c7fb602:vpc:8334f527-38e2-48d2-a7b5-a680bea0ca9a",
#     )

#     print(f"{import_cert_resp.json()}")

# except Exception as e:
#     print(f"Error has occurred: {e}")






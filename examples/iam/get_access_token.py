from krutrim_client import KrutrimClient
import traceback

client = KrutrimClient()  

try:
    resp = client.iam.signin_programmatic_user(
        account_id="enter the accountid",
        access_key="entet the access key",
        secret_key="enter the secret key",
    )

    token = resp.get("token") or resp.get("access_token")

    print("TOKEN:", token)

except Exception as e:
    print("Error:", repr(e))
    traceback.print_exc()


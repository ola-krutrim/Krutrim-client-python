from krutrim_client import KrutrimClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = KrutrimClient(api_key=api_key)

try:
    
    add_record = client.v1.record.create(


        krnid = "enter krn id ",
        rname = "enter record name ",
        value = "enter the value",                             #example 10.1.1.1
        ttl = 5,                                               #change as per requirement
        TYPE = "A"                                             #change as per requirement
    )

    print(f"Successfully added the record")

except Exception as e:
    print(f"Exception: {e}")

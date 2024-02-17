import os
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    myapikey = os.getenv("api_key")
    print(myapikey)
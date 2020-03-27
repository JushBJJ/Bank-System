import os
import json
import base64

def setup_file():
    # Use the file as a "database"
    if not os.path.exists("Accounts.txt"):
        format={}

        with open("Accounts.txt", "wb") as f:
            f.write(base64.b64encode(json.dumps(format).encode()))
    else:
        x=False

        with open("Accounts.txt", "rb") as f:
            try:
                x=json.loads(base64.b64decode(f.read()).decode())
            except:
                x=True
        
        if x==True:
            os.remove("Accounts.txt")
            setup_file()
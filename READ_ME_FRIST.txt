It is reccomended that you use the New Windows Terminal for this to work the best.

http://github.com/microsoft/terminal

How to Run:
python bank_system.py

Forgot your TFA_Code? Brute force your way in lol:

import hashlib
import random
import base64
import json

TFA_Code=""

with open("Accounts.txt", "rb") as f:
    x=json.loads(base64.b64decode(f.read()).decode())
    TFA_Code=x["Username"]["TFA_Code]

while True:
    code=""
    for i in range(5):
        code+=str(random.randint(0,9))
    if hashlib.blake2b(code.encode()).hexdigest()==TFA_Code:
        print("Code: "+code)

    
        break

Forgot your password? Brute force your way in too lol. But its gonna take a long time:
import hashlib
import json
import random
import string
import base64

correct=""

with open("Accounts.txt", "rb") as f:
    x=json.loads(base64.b64decode(f.read()).decode())
    correct=x["Username"]["Password"]

while True:
    password=""
    for i in range(random.randint(0,50)):
        password+=random.choice(string.printable)
    
    if hashlib.blake2b(password.encode()).hexdigest()==correct:
        print("Password: ", password)
        break
        
There are a lot better ways to do this though.

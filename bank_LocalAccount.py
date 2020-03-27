from bank_menu import print_options, clrscr, getKeyMenu, inpt
from bank_setup_file import setup_file

from datetime import datetime

import json
import time
import random
import base64
import hashlib

class LocalAccount:
    def __init__(self, info):
        # info has to be a dictionary/json
        # Credit Card Number: 16 Digits
        # Security Code: 4 digits
        # Phone: 10 Digits
        # TFA = 2 Factor Authenthiation 

        self.Format={
            "FirstName": "foo",
            "LastName": "foo",
            "Username": "foo",
            "Password": "foo",
            "CreditCardNumber": 0000000000000000,
            "SecurityCode": 0000,
            "Address": "Foo",
            "Postcode": 1234,
            "Email": "foo@exmaple.com",
            "Phone": 0000000000,
            "TFA": False,
            "TFA_Code": "0000000000",
            "Balance": 0,
            "TransactionLog":{}
        }

        self.Vaild=True

        if type(info) is dict:
            for x in self.Format.keys():
                if x not in info:
                    self.Vaild=False
            
        if self.Vaild==True:
            self.Account=info

            # Can be replaced with a for loop (future reference)
            self.Account["Balance"]=int(self.Account["Balance"])
            self.Account["Phone"]=int(self.Account["Phone"])
            self.Account["Postcode"]=int(self.Account["Postcode"])
            self.Account["SecurityCode"]=int(self.Account["SecurityCode"])
            self.Account["CreditCardNumber"]=int(self.Account["CreditCardNumber"])
        else:
            self.Account=None

    def get_value(self, value):
        try:
            return str(self.Account[value])
        except:
            return "N/A"

    def Deposit(self):
        clrscr()
        
        print_options(self.get_value("Username"), "Deposit", self.get_value("Address"), self.get_value("Balance"))
        print("Enter the amount you want to deposit. Enter any letter to go back.")

        x=inpt("> ")

        if x.isdigit():
            x=int(x)
            if x<=0:
                print("\033[91mYou can't deposit $", x, "\033[0m")
            else:
                self.append_transaction(f"Deposited ${x}.")
                self.Account["Balance"]+=x
                return
        else:
            return

        self.update_account()
        inpt("Press \033[91menter\033[0m to continue")

    def Withdraw(self):
        clrscr()

        print_options(self.get_value("Username"), "Withdraw", self.get_value("Address"), self.get_value("Balance"))
        print("Enter the amount you want to withdraw. Press any letter to go back.")
        x=inpt("> ")

        if x.isdigit():
            x=int(x)
            if x<=0:
                print(f"\033[91mYou can't withdraw ${x}\033[0m")
            elif x>int(self.get_value("Balance")):
                print("\033[91mInsufficient Funds.\033[0m")
            else:
                self.append_transaction(f"Withdrawed ${x}.")
                self.Account["Balance"]-=x
                return
        else:
            return

        self.update_account()
        inpt("Press \033[91menter\033[0m to continue")

    def show_all_info(self):
        clrscr()
        
        for key, value in self.Account.items():
            if key=="TransactionLog" or key=="TFA_Code" or key=="Password" or key=="CreditCardNumber" or key=="SecurityCode":
                continue
            
            print(f"\033[93m{key}\033[0m: {value}")

        inpt("Press \033[91menter\033[0m to continue")

    def TFA(self):
        print_options(self.get_value("Username"), "Two Factor Authenthication", self.get_value("Address"), self.get_value("Balance"))
        if self.Account["TFA"]=="True":
            self.Account["TFA"]="False"
            print("\033[92m2FA Disabled.\033[0m")
            inpt("Press \033[91menter\033[0m to continue.")

        else:
            new_code=""
            for _ in range(5):
                new_code+=str(random.randint(0,9))
            
            self.Account["TFA_Code"]=hashlib.blake2b(new_code.encode()).hexdigest()
            print(f"\033[92mTFA Enabled\033[0m, your code is \"\033[93m{new_code}\033[0m\"")
            
            inpt("Press \033[91menter\033[0m when you've written down/remembered your TFA Code.")
            self.Account["TFA"]="True"
        self.update_account()

    def New_Password(self):
        print_options(self.get_value("Username"), "New Password", self.get_value("Address"), self.get_value("Balance"))

        while True:
            x=inpt("Your new password: ")
            c=inpt("Confirm new password: ")

            if x==c:
                self.Account["Password"]=hashlib.blake2b(x.encode()).hexdigest()
                print("\033[92mYou password changed!\033[0m")
                inpt("Press \033[91mEnter\033[0m to continue")
                break

            else:
                print("\033[91mYour confirmed password input doesn't match your new password! Please try again\033[0m")
        
        self.update_account()

    def New_Phone(self):
        print_options(self.get_value("Username"), "New Phone", self.get_value("Address"), self.get_value("Balance"))

        while True:
            c=inpt("Your new phone number: ")

            if any(x.isdigit() for x in c) == True and len(c)==10:
                self.Account["Phone"]=int(c)
                print("\033[92mPhone number changed!\033[0m")
                inpt("Press \033[91mEnter\033[0m to continue")
                break

            else:
                print("\033[91mInvaild phone number. Your number must have 10 digits.\033[0m")
        
        self.update_account()

    def security(self):
        while True:
            clrscr()
            
            self.options={
                "Enable/Disable 2 Factor Authenthication":self.TFA,
                "Open Transaction Log":self.show_transaction,
                "Change Password":self.New_Password,
                "Change Phone Number":self.New_Phone,
                "Back":"return"
            }   
        
            print_options(self.get_value("Username"), "Security", self.get_value("Address"), self.get_value("Balance"),self.options)

            if getKeyMenu(self.options)=="return":
                return True
        return False
        
    def Settings(self):
        while True:
            clrscr()
            
            self.options={
                "Account Info":self.show_all_info,
                "Security":self.security,
                "Exit":"return"
            }
            print_options(self.get_value("Username"), "Settings", self.get_value("Address"), self.get_value("Balance"), self.options)
            if getKeyMenu(self.options)=="return":
                return True
        return False

    def Home(self):
        while True:
            clrscr()

            self.options={
                "Deposit Money": self.Deposit,
                "Withdraw Money": self.Withdraw,
                "Settings":self.Settings,
                "Back": "return"
            }

            print_options(self.get_value("Username"), "Home", self.get_value("Address"), self.get_value("Balance"), self.options)
            if getKeyMenu(self.options)=="return":
                return True
        return False

    def update_account(self):
        setup_file()

        # Temporary solution
        with open("Accounts.txt", "rb") as f:
            local_accounts=json.loads(base64.b64decode(f.read()).decode())
            local_accounts[self.Account["Username"]]=self.Account

        with open("Accounts.txt", "wb") as f:
            f.write(base64.b64encode(json.dumps(local_accounts).encode()))
    
    def append_transaction(self, action):
        time=str(datetime.now())
        ID=len(self.Account["TransactionLog"])

        self.log=f"{time}\nID {ID}) {action}"
        self.Account["TransactionLog"][str(ID)]=self.log

        self.update_account()
    
    def show_transaction(self):
        clrscr()

        print("\033[93mTransaction Log\033[0m")
        x=0
        for i in self.Account["TransactionLog"].values():
            print(i.replace(f"ID {x})", f"\033[94mID {x})\033[0m\n"))
            x+=1
        
        inpt("Press \033[91menter\033[0m to exit.")
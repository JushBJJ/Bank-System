try:
    import json
    import os
    import time
    import random
    import hashlib
    import re
    import sys
    import base64
    import hashlib

    from colorama import init, Fore, Back, Style, Cursor
    from bank_menu import print_options, clrscr, print_menu, getKeyMenu, inpt
    from bank_setup_file import setup_file
    from bank_LocalAccount import LocalAccount

except:
    print("""
Please sure you have these python libraries installed:
    - json
    - os
    - time
    - random
    - hashlib
    - colorama
    - re
    - sys
    - base64
    - hashlib

And you have these files:
    - bank_menu.py
    - bank_setup_file.py
    - bank_LocalAccount.py

    If you have these files/libraries and the program still isnt't working, then the program has a source code error. Try to fix it.
""")
    exit(0)
        
def Login():
    clrscr()
    print("""
\033(0qqqqq\033(B
\033[93mLogin\033[0m
\033(0qqqqq\033(B
Input \"\033[91m-1\033[0m\" to go back. Enter of the following information...
""")

    username=inpt("\033[93mUsername: \033[0m")
    if username=="-1":
        return False

    print("\033(0qqqqqqqqqqq\033(B")

    password=inpt("\033[93mPassword: \033[0m")
    if password=="-1":
        return False
    
    setup_file()

    with open("Accounts.txt", "rb") as f:
        Accounts=f.read()
        Accounts=json.loads(base64.b64decode(Accounts).decode())

    if username in Accounts.keys():
        LocalAcc=LocalAccount(Accounts[username])
        if LocalAcc.Vaild and hashlib.blake2b(password.encode()).hexdigest()==LocalAcc.Account["Password"]:
            if LocalAcc.Account["TFA"]=="True":
                while True:
                    tfa_code=inpt("\033[93m2FA Code: \033[0m")

                    if hashlib.blake2b(tfa_code.encode()).hexdigest()==LocalAcc.Account["TFA_Code"]:
                        LocalAcc.Home()
                        break
                    elif tfa_code=="-1":
                        return False
                    else:
                        print("\033[91mInvaild 2FA Code.\033[0m")
                        continue
            else:
                LocalAcc.Home()
        elif LocalAcc.Vaild and LocalAcc.Account["Password"]!=hashlib.blake2b(password.encode()).hexdigest():
            print("\033[91mIncorrect password.\033[0m")
            inpt("Press Enter to continue.")
            return False
        else:
            print("\033[91mYour account has invaild account information. Please register again.\033[0m")
            inpt("Press Enter to continue.")
            return False
    else:
        print("\033[91mThis account does not exist, make sure you register this account before you log in again.\033[0m")
        inpt("Press Enter to continue.")
        return False
    
    return True

def reg_ask(value, n):
    requirements={
        "CreditCardNumber":16,
        "SecurityCode":4,
        "Postcode":4,
        "Phone":10
    }

    z=""
    x=inpt("\033[93m"+value+"\033[0m")
    if x=="-1":
        return False

    for i in n:
        if i.isupper():
            z+=' '
        z+=i

    if (x.isalnum() or x.isdigit())==False and ("@" or ".") not in x:
        print("\033[91mYou can only type letters or numbers. (No spaces, symbols, etc)\033[0m")
        return True

    elif n=="CreditCardNumber" or n=="SecurityCode" or n=="Postcode" or n=="Phone":
        if not x.isdigit():
            print("\033[91mValue", z, " needs to be a number. (No letters, spaces, symbols...)\033[0m")
            return True
        elif n=="CreditCardNumber" and len(x)!=16 or (n=="Postcode" and len(x)!=4) or (n=="Phone" and len(x)!=10) or (n=="SecurityCode" and len(x)!=4):
            print("\033[91mValue ", z, " needs a total of", requirements[n], " digits.\033[0m")
            return True

    elif n=="FirstName" or n=="LastName":
        if x.isdigit():
            print("\033[91mValue ", z, " should not have digits.\033[0m")
            return True

    elif x.isdigit() and n!="Password":
            print("\033[91mValue ", z, "should not have digits.\033[0m")
            return True

    elif n=="Username":
        setup_file()

        with open("Accounts.txt", "rb") as f:
            z=json.loads(base64.b64decode(f.read()).decode())

            if x in z.keys():
                print("\033[91mUsername already taken.\033[0m")
                return True
    elif n=="Email":
        if bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", x))==False:
            print("\033[91mInvaild email. Example: example@example.com\033[0m")
            return True
    return x

def Register():
    clrscr()
    Account={}

    inputs={
        "First Name: ":0,
        "Last Name: ":1,
        "Username: ":2,
        "Password: ":3,
        "Credit Card Number: ":4,
        "Security Code: ":5,
        "Address: ":6,
        "Postcode: ":7,
        "Email: ":8,
        "Phone: ":9
    }

    print("""
\033(0qqqqqqqq\033(B
\033[93mRegister\033[0m
\033(0qqqqqqqq\033(B
Input \"\033[31m-1\033[0m\" to go back. Enter the following information...
""")

    Account["TFA"]="False"
    Account["Balance"]="0"
    Account["TFA_Code"]="0000000000"
    Account["TransactionLog"]={}

    for i in inputs:
        n=(i.replace(": ", "")).replace(" ","")
        while True:
            Account[n]=reg_ask(i, n)
            if Account[n]==False:
                return False
            elif Account[n]==True:
                continue
            break
    
    setup_file()

    with open("Accounts.txt", "rb") as f:
        x=json.loads(base64.b64decode(f.read()).decode())

    with open("Accounts.txt", "wb") as fs:
        Account["Password"]=hashlib.blake2b(Account["Password"].encode()).hexdigest()
        x[Account["Username"]]=Account
        fs.write(base64.b64encode(json.dumps(x).encode()))

    LocalAcc=LocalAccount(Account)
    if LocalAcc.Vaild==True:
        LocalAcc.Home()
    return False

def main():
    while True:
        clrscr()
        options={
            "Login":Login,
            "Register":Register,
            "Exit":exit
        }

        print("""
\033(0qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq\033(B
\033[93mWelcome to the bank of The Boring Company.\033[0m
\033(0qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq\033(B
Use the \033[91mArrow Keys\033[0m to navigate through the options and press \033[91mEnter\033[0m to select an option.
""")
        print_menu(options)
        if getKeyMenu(options)=="return":
            break
    return

if __name__ == "__main__":
    clrscr()
    print("It's highly reccomended to use terminals that support ANSI.\n\nTerminals like:\n\tVisual Studio Code Integrated Terminal\n\tThe NEW Windows Terminal (https://github.com/microsoft/terminal)\n\nIs highly reccomended to use for this program to work perfectly.")
    print("Press Enter 3 times.")

    for _ in range(3):
        inpt(f"Press Enter to continue. [{_}]")

    init()
    main()
"""
References:
    - https://en.wikipedia.org/wiki/ANSI_escape_code
    - https://ozzmaker.com/add-colour-to-text-in-python/
    - https://voidinit.com/python/console/files
    - https://docs.python.org/3/library/json.html
    - http://www.json.org/example.html
    - https://docs.python.org/3/library/functions.html#any
    - https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences
    - Current python Knowledge

Mindmap: https://www.draw.io/#HJushBJJ%2FDigital-Technology-Highschool%2Fmaster%2Fgrade%209%2FBank

Update Log/Improvements:
    - 3/3/2020:
        1: Made base bank account class 
        2: Made Login function
        3: Made main function
        4: Made Register function
        5: Fixed dictionary error "undefined variable "x" (forgot to put quotation marks)
        6: Changed clrscr() to clrscr() because "clear" is usually only for Linux/MacOS and cls is the comman for clear in Windows/NT
        7: Note: ANSI printing will replace the normal inputting once all functions roughly done
        8: After main function is returned, the text will go back to normal (for future references)
        9: Made `-1` input to be the back option in input/register function
        10: Added file IO in input and register for reading/writing accounts in the Accounts.txt file
        11: Adjusted default accounts JSON format from:
            {
                "Accounts":{

                }
            }
        to...
            {}
        to increase simplicity in the code
        12: Added code to check if user exists or not.
        13: Added Home() function in LocalAccount class

    - 4/3/2020:
        14: Fixed incorrect format checking for checking if the account has the right formats.
        15: Made basic registration
        16: Fixed registration invaild formats
        17: Fixed vaild format checking
        18: Finished regristration
        19: Fixed account info checking.

    - 5/3/2020:
        20: Added Basic Deposit System
        21: Added Basic Withdraw System
        22: Added print_options function
        23: Added settings function
        24: Added account_info function
        25: Addded security function

    - 6/3/2020
        26: Improved registration, when a user gets something incorrect, it asks the user to attempt to input the value again
        27: Added update_account function so balance is updated when someone withdraws/deposits
        28: Checked if password is correct or incorrect
        29: Removed useless print functions that was only purposed for testing
        30: Fixed update_account function that prints the account information into file
        31: Added fix that if the json file is invaild/empty, it will error. Instead it will now make a new file.
    
    - 8/3/2020:
        32: Added check for registering if the username is the same
        33: Added Security Function
        34: Enabled 2FA and added security settings
        35: Fixed Login
        36: Fixed bug where it keeps looping the 2FA input after exiting
    
    - 12/3/2020:
        37-46: Added menu selection using arrow keys

    - 14/3/2020:
        47: Added tranaction log

    - 15/3/2020:
        35: Implemented ANSI, menu selections, etc
        36: Organized files
        37: Added transaction log functions and implemented them on deposit, withdraw
        38: Added new menu selection in security thing to show transaction logs
        39: Made menu selection go to the last option if arrow key pressed up when the selected menu is the first one

    - 20/3/2020:
        40: Added custom input function to prevent user from pressing arrow keys in normal prompts
        41: Fixed account info showing transactionlog json
        42: Fixed email checking
        43: Added backspace support for custom input 
        44: Fixed typing "-" wont input through
        45: Added buffer limit
        46: Tweaked login
    
    - 24/3/2020:
        47: Did a little experiment, switched from recursion to loops.

    - 26/3/2020:
        48: Added hashing, and basic security
        49: Removed show account info function from showing some personal information like passwords

Test Log:
    1: When I try to delete the Accounts.txt file, it errors
    2: When I use certain ANSI codes, it breaks on terminals that don't suppport ANSI
    3: When the json file is invaild, the program breaks
    4: When I try to exit a certain section, it exits instead of going back to login
    5: When the account is invaild, it errors
    6: When I try to write an invaild email, it accepts it
    7: When I try to input nothing for login, it errors
    8: When the program automatically updates the file/fixes the file, it errors/clears the file.
    9: When I register in the same username, it will create a new account without checking and overwrite the exiting account
    10: When I try to spam arrow keys, depending on the computer peformance, it lags due to it clearing and rewriting.
    11: Account checking errors
    12: The program somehow invaildly formats the account dictionary
    13: When someone incorrectly inputs invaild registration value, it exits out instead of asking again
    14: After withdraw/deposit, it doesn't update.
    15: When a person logs in, it doesnt check the password
    16: 2FA keeps looping
    17: 2FA in login keeps making it invaild.
    18: When trying to list out the transaction log, it will only print out numbers.
    19: Account Info shows transaction logs when it shouldnt.
    20: When I press arrow keys in a normal prompt, the terminal goes through its command/input history.
    21: When backspace is pressed on custom input, the cursor goes backwards and doesnt do anything else
    22: When I press ctrl + any letter, it will print out external symbols
    23: When I press tab then backwards, it goes to pos(1,1)
    24: When I press "-" it doesn't print out.
    25: When I press '." it doesnt print out.
    26: When I type a vaild email, it errors
    27: Program doesn't automatically clear buffer before asking for input
    28: Program prints out the next string (from print)
    29: When a user prints out a big string, it buffers to the next line in login.
    30: A user tries to select password instead of pressing enter first.
    31: When I press "enter" in register then enter "-1", it errors.
    32: While trying to switch from recursion to loops, when i press the arrow button it goes back to the main menu

Test Log:
    (3/3/2020):
        #1: Tested multiline print 
        #2: Tested ANSI escape codes (shell)
        #3: Tested JSON formatting and file IO
        #4: Tested file IO reading, converting the contents into json and printing the value
        #5: Tested if printing a specific dictionary value (eg. Accounts["John"]["Phone"]) works.
        #6: Tested the new plain json format ({})
        #7: Tested if value from dictionary does/doesn't exist
    (4/3/2020):
        #8: Testing for account vaildation
        #9: Login Test
        #9: Tested regristration
        #10-20: Tested registration 

    (5/3/2020):
        #21: Login Test
        #22: Deposit test
        #23: Withdraw test
        #24: Tested tweaked registration
        #25: Tested login (password)
        #26: Tested Account Info function
    
    (6/3/2020):
        #27: Tested fix for updating account information into file
        #28: Tested update_account function
    
    (8/3/2020):
        #29: Tested register using the same username
        #30: Tested security options and 2FA
        #31: Tested login fix
        #32: Tested 2FA
        #33: Tested password change
        #34: Tested phone number change
    
    (12/3/2020):
        35-46: Tested menu selection using arrow keys

    (14/3/2020):
        47: Tested tranaction log
        48: Tested menu selection

    (15/3/2020):
        35: Tested ANSI, menu selections
        36: Tested linking files
        37: Tested transaction log
        38: Tested "Made menu selection go to the last option if arrow key pressed up when the selected menu is the first one"

    (20/3/2020):
        39: Tested custom input function
        40: Tested account info fix
        41: Tested buffer limit
        42: Fixed registration error.
    
    (21/3/2020):
        43: Tweaked phone change, password change, deposit, withdraw and 2FA.
        44: Code improvement

    (24/3/2020):
        45: Tested loops
    
    (26/3/2020):
        46: Tested base64 and hashing on accounts

Features:
    - Login
    - Register
    - Register multiple different accounts
    - 2FA
    - Withdraw
    - Deposit
    - Change Password
    - Change Phone number
    - Settings
    - Show account info
    - Basic Security
    - Transaction Log
    - Custom input function

Improvements - what else needs to be done:
    - Encryption or Hashing

### Bank

# Algorithm for pre-main

CLEAR SCREEN
PRINT(It's highly reccomended to use terminals that support ANSI.\n\nTerminals like:\n\tVisual Studio Code Integrated Terminal\n\tThe NEW Windows Terminal (https://github.com/microsoft/terminal)\n\nIs highly reccomended to use for this program to work perfectly.)
PRINT("Press Enter 3 times.")

FOR 0 TO 3
    PRINT "Press enter to continue [NUMBER]"
    INPUT ENTER

BEGIN COLORAMA INITIALIZATION
BEGIN MAIN FUNCTION

# Algorithm for main

WHILE TRUE
    CLEAR SCREEN
    LET OPTIONS = DICTIONARY{
        "Login":LOGIN_FUNCTION,
        "Register":REGISTER_FUNCTION,
        "Exit":EXIT_FUNCTION
    }

    PRINT MAIN INTERFACE

    BEGIN PRINT_MENU(OPTIONS)

    IF GETKEYMENU_FUNCTION(OPTIONS) EQUALS "return"
        BREAK LOOP

# Algorithim for Login
    CLEAR SCREEN
    PRINT LOGIN INTERFACE

    INPUT USERNAME
    
    IF USERNAME IS EQUAL TO "-1"
        RETURN FALSE
    
    PRINT LINE

    INPUT PASSWORD

    IF PASSWORD IS EQUAL TO "-1"
         RETURN FALSE
        
    BEGIN SETUP_FILE

    LOAD FILE
    LET ACCOUNTS = PARSED JSON CONTENT

    IF USERNAME IS IN ACCOUNTS.KEYS()
        LET LOCALACC = LOCALACCOUNT INIT

        IF LOCALACC IS VAILD AND PASSWORD EQUALS TO THE ACCOUNT PASSWORD
            IF TWO FACTOR AUTHENTHICATION IS ENABLED IN THE LOCALACC
                WHILE TRUE
                    LET TFA_CODE EQUAL TO USER INPUT

                    IF TFA_CODE IS EQUAL TO THE LOCALACC TFA_CODE
                        BEGIN LOCALACC.HOME()
                        BREAK
                    ELSE IF TFA_CODE IS "-1"
                        RETURN FALSE
                    ELSE
                        PRINT("INVAILD 2FA CODE")
                        CONTINUE
            ELSE
                BEGIN LOCALACC.HOME()
        ELSE IF LOCALACC.VAILD IS TRUE AND LOCALACC PASSWORD IS DOES NOT MATCH
            PRINT("INCORRECT PASSWORD")
            PRINT("PRESS ENTER TO CONTINUE")
            INPUT 
            
            RETURN FALSE
        ELSE
            PRINT("YOUR ACCOUNT HAS INVAILD ACCOUNT INFORMATION")
            PRINT("PRESS ENTER TO CONTINUE")
            INPUT

            RETURN FALSE
    ELSE
        PRINT("THIS ACCOUNT DOES NOT EXIST, MAKE SURE YOU REGISTER THIS ACCOUNT BEFORE YOU LOGIN AGAIN")
        INPUT

        RETURN FALSE
    RETURN TRUE

# Algorithm for Register

    CLEAR SCREEN
    LET ACCOUNT = EMPTY DICTIONARY
    LET INPUTS = NORMAL ACCOUNT DICTIONARY

    PRINT REGISTER INTERFACE

    DEFINE TFA, BALANCE, TFA_CODE AND TRANSACTIONLOG INTO ACCOUNT
    
    FOR EVERY INPUT
        LET N = REPLACE ": " INTO "" AND " " INTO ""

        WHILE TRUE
            ACCOUNT VALUE OF N IS EQUAL TO REG_ASK FUNCTION

            IF ACCOUNT VALUE IS FALSE
                RETURN FALSE
            ELSE IF ACCOUNT VALUE IS TRUE
                CONTINUE
            BREAK
    
    BEGIN SETUP_FILE()

    OPEN Accounts.txt FILE
        LET x = PARSE FILE CONTENT INTO JSON

    OPEN Accounts.txt FILE
        CREATE/CLEAR FILE
        LET ACCOUNT USERNAME OF X = ACCOUNT

        WRITE PARSED JSON CONTENT OF X WITH INDENT OF 4
    
    LET LocalAcc = LOCALACCOUNT INIT

    IF LOCALACC IS VAILD
        BEGIN LOCALACC.HOME()
    
    RETURN FALSE

# Algorithm for Deposit
BEGIN CLEAR_SCREEN
BEGIN PRINT_OPTIONS(ACCOUNT_USERNAME, "Deposit", ADDRESS, ACCOUNT_BALANCE)

PRINT "Enter the amount you want to deposit. Enter any letter to go back."
LET x = INPT("> ")

IF HAS DIGIT IN STRING x
    x=INT(x)

    IF x <= 0
        PRINT("You can't deposit $x")
    ELSE
        BEGIN APPEND_TRANSACTION("Deposited $x")
        CALCULATE BALANCE=BALANCE+x
ELSE
    RETURN

BEGIN UPDATE_ACCOUNT
BEGIN INPT("Press enter to continue")

# Algorithm for Withdraw
BEGIN CLEAR SCREEN
BEGIN PRINT_OTPTIONS(ACCOUNT_USERNAME, "Withdraw", ADDRESS, ACCOUNT_BALANCE)

PRINT "Enter the amount you want to withdraw. Enter any letter to go back."

IF HAS DIGIT IN STRING x
    x=INT(x)

    IF x <= 0
        PRINT "You can't withdraw $x"
    ELSE IF x>INT(ACCOUNT_BALANCE)
        PRINT "Insufficient Funds."
    ELSE
        BEGIN APPEND_TRANSACTION("Deposited $x")
        CALCULATE BALANCE=BALANCE-x
        RETURN
ELSE
    RETURN

BEGIN UPDATE_ACCOUNT
BEGIN INPT("Press enter to continue")

"""
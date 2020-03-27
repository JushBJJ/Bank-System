from colorama import init, Cursor
from msvcrt import getch

left=lambda n=1: print("\033[D", end="")

npos=Cursor.POS
cpos={"x":1, "y":1}
selected_menu=1

buffer=""

def print_options(username, section, address, balance, options=None):
    clrscr()
    print("""
{username} \033(0x\033(B \033[93m{section}\033[0m \033(0x\033(B {address}
\033[92mBalance\033[0m: {balance}
    """.format(username=username, section=section, address=address, balance=balance))

    # Assuming options argument is a dictionary
    if options!=None:
        print_menu(options)

def print_menu(options):
    n=1
    for key in options.keys():
        if n==selected_menu:
            print("\033[47;30m", end="")
        else:
            print("\033[0m", end="")

        print("{n}) {key}\033[0m".format(n=n, key=key))
        n+=1

def pos(x,y, m=""):
    global cpos

    if x<1:
        x=1
    if y<1:
        y=1

    cpos["x"]=x
    cpos["y"]=y

    if m=="":
        print(npos(cpos["x"],cpos["y"]), end="")
    else:
        print(npos(cpos["x"],cpos["y"]), m, end="")
        cpos["x"]=x+len(m)
        cpos["y"]=y
        pos(cpos["x"]-len(m), cpos["y"])
    
def inpt(prompt):
    global buffer
    clear_buffer()

    counter=0

    if prompt==None:
        prompt=""

    print(prompt, end="")

    while True:
        x=getch()

        if x==b"\x08":
            buffer=buffer[0:len(buffer)-1]
            counter-=1

            if counter>=0:
                left()
                print(" ", end="")
                left()

        elif ord(x)<ord("0") and x!=b"-" and x!=b"." and x!=b"\r" and x!="\t":
            if x==b"\x00":
                x=getch()
            continue

        elif x==b"\t":
            continue

        else:
            if x==b"\r":
                x=buffer

                clear_buffer()
                print("")
                return x
            elif counter<0:
                counter=0
                clear_buffer()

            if (ord(x)>=ord("0") and ord(x)<=ord("z")) or x==b"-" or x==b".":
                if counter==50:
                    continue
                
                print(chr(ord(x)), end="")
                buffer+=chr(ord(x))
                counter+=1
        
        continue
    return buffer

def clear_buffer():
    global buffer

    buffer=""
    
def getKeyMenu(options):
    global selected_menu
    x=getch()

    if x == b"\x00":
        x=getch()  
        if x==b"H":
            selected_menu-=1

            if selected_menu<1:
                selected_menu=len(options.keys())
            
            return selected_menu
            
        elif x==b"P":
            selected_menu+=1
            
            if selected_menu>len(options.keys()):
                selected_menu=1
            
            return selected_menu
    elif x==b"\r":
        if inpt==True:
            return "return"

        x=1
        for i in options.keys():
            if x==selected_menu:
                selected_menu=1
                if options[i]=="return":
                    return "return"
                else:
                    return options[i]()
            x+=1

def clrscr():
    print("\033[2J")
    pos(1,1)
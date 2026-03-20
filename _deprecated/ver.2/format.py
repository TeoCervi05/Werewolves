#there is a possibility to convert this simple script in a library
import textwrap
import os
from log import log_this

def check_size():
    return os.get_terminal_size().columns

#--FORMATTED PRINTS

#preformatted output
def prints(text, style = ""):
    
    #QUICK STYLE LEGEND:
    #"title": titles;
    #"stitle": subtitles;
    #"head": headings;
    #"bull": bullet list;
    #"err": errors;
    #None: standard text.

    #titles
    if style == "title":
        print(f"\n === {text.upper()} ===")
        return

    #subtitles    
    if style == "stitle":
        print(f"\n -- {text.upper()} --")
        return

    #heading
    if style == "head":
        print(f"\n {text.upper()}")
        return
 
    #body
    if style == "body":
        print(f"  {text}")
        return

    #bullet list
    if style == "bull":
        bullet_list = text.split("_")
        for l in bullet_list:
            rows = textwrap.wrap(l, check_size() - 4)
            i = 0
            for r in rows:
                if i == 0:
                    print(f"  - {r}")
                    i = i + 1
                else:
                    print(f"    {r}")
        return
    
    #error
    if style == "err":
        print(f"  !ERROR: {text}!")
        log_this("error", f"{text}.")
        return

    #standard text
    rows = textwrap.wrap(text, check_size() - 3)
    for r in rows:
        print(f"   {r}")
    return

#preformatted input
def printq(text = "", _type = "", min = 0, max = 0, opt = []):
    #check return
    
    #int
    if _type == "int":
        while True:
            try:
                return int(input(f"\n {text} (int) > "))
            
            except:
                prints("an \"int\" input was expected", "err")

    #range
    if _type == "range":
        while True:
            try:
                ans = int(input(f"\n {text} (int, {min}:{max}) > "))
                if ans < min or ans > max:
                    prints(f"answer must be in range {min} to {max}", "err")
                else:
                    return ans
            
            except:
                prints("an \"int\" input was expected", "err")

    #list
    if _type == "list":
        i = 0
        for o in opt:
            prints(f"[{i + 1}] {o}", "bullet")
            i = i + 1
        i = printq(text, "range", 1, i) - 1
        return opt[i]
    
    #no check
    if text == "":
        return input(f"\n > ")
    
    return input(f"\n {text} > ")

#preformatted help tabs
def printh(query, desc, syntax, params):
    size = check_size()
    print("")
    print((" *" * (size // 2))[:size])
    prints(query, "stitle")

    #query
    prints("query:","head")
    prints(f"{desc}")

    #syntax
    prints("syntax:","head")
    prints(syntax, "body")

    #tags and parameters
    prints("tags and parameters:", "head")

    if params[0] == None:
        prints("There are no tags nor parameters for this query.")

    else:
        for p in params:
            prints(f"{p[0]}:", "body")
            prints(f"{p[1]}")

    print("")
    print((" *" * (size // 2 + 1))[:size])

#def printq(text = "", ret = ""):

#    valid = 0

#    while not valid:

#        ans = input(f" {text} {ret} > ") if not ret == "" else ans = input(f" {text} >")

#        if ret == "bool":

#            if ans.upper() == "Y" or ans == "1":

#                return 1

#            else:

#                return 0

        #change int to id, add index list 

#        if ret == "int":

#            try:

#                ans = int(ans)

#                return ans

#            except:

#                prints("Warning, your answer is not valid", "error")

#        else:

#            return ans
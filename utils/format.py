import textwrap
import os

# TO DO: in printer, add an option to simulate /n

def shell_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80

def printer(rows, spaces = 0):
    for r in rows:
        print(f" " * spaces + r)

# -- FORMATTED PRINTS --

def printf(text, style = ""):
    width = shell_width()
    
    #titles
    if style == "title":
        printer(textwrap.wrap(f"\n=== {text.upper()} ===", width), 1)
        return

    #standard
    printer(textwrap.wrap(text, width - 3), 3)
import textwrap
import os

# TO DO: in printer, add an option to simulate /n

def shell_width():
    try:
        return os.get_terminal_size().columns
    
    except OSError:
        return 80

def printer(rows, spaces = 0, newline = False):
    if newline:
        print("")

    for r in rows:
        print(f" " * spaces + r)

# -- FORMATTED PRINTS --

def printf(text, style = ""):
    width = shell_width()

    """
    LEGEND:
    title - title;
    body - (leave empty).
    """
    
    #titles
    if style == "title":
        print(textwrap.wrap(f"=== {text.upper()} ===", width)[0])
        return

    #standard
    printer(textwrap.wrap(text, width - 3), 3)

def printq(text):
    # no check
    if text == "":
        return input(f"\n > ").strip()

    return input(f"\n {text} > ").strip()
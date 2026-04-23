import textwrap
import os

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
    subtitle - stitle;
    heading - head;
    body - body;
    basic text - (leave empty, or type anything but the aboves).
    """
    
    #titles
    if style == "title":
        printer(textwrap.wrap(f"=== {text.upper()} ===", width - 1), 1, True)
        return

    #subtitles
    if style == "stitle":
        printer(textwrap.wrap(f"-- {text.upper()} --", width - 1), 1, True)
        return

    #heading
    if style == "head":
        printer(textwrap.wrap(f"{text.upper()}", width - 1), 1, True)
        return

    #bullet
    if style == "bull":
        text_list = text.split("_")
        for t in text_list:
            printer(textwrap.wrap(f"- {t}", width - 2), 2)
        return

    #body
    if style == "body":
        printer(textwrap.wrap(text, width - 2), 2)
        return

    #error
    if style == "err":
        printer(textwrap.wrap(f"ERROR: {text}", width), 0)
        return

    #standard
    printer(textwrap.wrap(text, width - 3), 3)

def printq(text = ""):
    # no check
    if text == "":
        return input(f"\n > ").strip()

    return input(f"\n {text} > ").strip()
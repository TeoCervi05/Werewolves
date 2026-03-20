import textwrap
import os

def get_terminal_width():
    # English: helper to safely obtain terminal width, fallback to 80 if unavailable.
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80

# -- FORMATTED PRINTS

# preformatted output
def prints(text, style=""):
    """
    Pretty-print text to terminal using simple styles.
    Style values: "title", "stitle", "head", "body", "bullet", "err"
    """
    # titles
    if style == "title":
        print(f"\n === {text.upper()} ===")
        return

    # subtitles
    if style == "stitle":
        print(f"\n -- {text.upper()} --")
        return

    # heading
    if style == "head":
        print(f"\n {text.upper()}")
        return

    # body
    if style == "body":
        print(f"  {text}")
        return

    # bullet list
    if style == "bullet":
        bullet_list = text.split("_")
        width = get_terminal_width()
        for l in bullet_list:
            rows = textwrap.wrap(l, width - 4)
            first = True
            for r in rows:
                if first:
                    print(f"  - {r}")
                    first = False
                else:
                    print(f"    {r}")
        return

    # error
    if style == "err":
        print(f"  !ERROR: {text}!")
        # Logging errors is optional and performed by the caller if desired to avoid circular imports.
        return

    # standard text
    width = get_terminal_width()
    rows = textwrap.wrap(text, width - 3)
    for r in rows:
        print(f"   {r}")
    return

# preformatted input
def printq(text="", _type="", min=0, max=0, opt=None):
    """
    Prompt wrapper. Supports types: "", "int", "range", "list".
    opt is used for list type.
    """
    if opt is None:
        opt = []

    # int
    if _type == "int":
        while True:
            try:
                return int(input(f"\n {text} (int) > "))
            except ValueError:
                prints("an \"int\" input was expected", "err")

    # range
    if _type == "range":
        while True:
            try:
                ans = int(input(f"\n {text} (int, {min}:{max}) > "))
                if ans < min or ans > max:
                    prints(f"answer must be in range {min} to {max}", "err")
                else:
                    return ans
            except ValueError:
                prints("an \"int\" input was expected", "err")

    # list
    if _type == "list":
        i = 0
        for o in opt:
            prints(f"[{i + 1}] {o}", "bullet")
            i = i + 1
        i = printq(text, "range", 1, i) - 1
        return opt[i]

    # no check
    if text == "":
        return input(f"\n > ").strip()

    return input(f"\n {text} > ").strip()

# preformatted help tabs
def printh(query, desc, syntax, params):
    size = get_terminal_width()
    print("")
    print((" *" * (size // 2))[:size])
    prints(query, "stitle")

    # query
    prints("query:", "head")
    prints(f"{desc}")

    # syntax
    prints("syntax:", "head")
    prints(syntax, "body")

    # tags and parameters
    prints("tags and parameters:", "head")

    if params[0] is None:
        prints("There are no tags nor parameters for this query.")

    else:
        for p in params:
            prints(f"{p[0]}:", "body")
            prints(f"{p[1]}")

    print("")
    print((" *" * (size // 2 + 1))[:size])
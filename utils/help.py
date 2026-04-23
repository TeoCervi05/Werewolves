from utils.format import shell_width, printf

# preformatted help tabs
def printh(query, desc, syntax, params):
    size = shell_width()
    print("")
    print((" *" * (size // 2))[:size])
    printf(query, "stitle")

    # query
    printf("query:", "head")
    printf(f"{desc}")

    # syntax
    printf("syntax:", "head")
    printf(syntax, "bull")

    # tags and parameters
    printf("tags and parameters:", "head")

    if params[0] is None:
        printf("There are no tags nor parameters for this query.", "body")

    else:
        printf(params, "bull")

    print("")
    print((" *" * (size // 2 + 1))[:size])

def system_help(query):
    if query == "help":
        printh(
            "help",
            "This query is designed for beginners, like you, that doesn't know how to use this program. It can be used alone, or combined with other queries to receive a meticoulus description on how that command works and how it can be used. I don't honestly know why on Earth you choose to use this query on itself: it seems like a very dumb thing if you ask me, but I'm doing my best to explain.",
            "help_help {query}",
            "{query}: like you just did, write the command you want to get help about to discover such interesting things on it."
        )
        return

    if query == "quit":
        printh(
            "quit",
            "This is the most important query of all: it is always the first to be impemented in every program even when written by beginners. Whitout this query, the program would go into an infinite loop that nothing but some brutal methods like \"forced shutdown\" or \"reboot\" would be able to stop. Luckly, I thinked of a way to easily close the program, how smart am I? ;-)",
            "quit_quit {param}",
            "-d or -delete: use it only if you are not accessing this session anymore: this will purge the game database. NOT IMPLEMENTED YET"
        )
        return

    printf(f"unknown command \'{query}\'", "err")
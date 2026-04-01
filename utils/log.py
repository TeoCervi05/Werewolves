import os
from datetime import datetime

LOG_NAME = "log/log.txt"

def log_this(title, desc):
    timestamp = datetime.now().isoformat(timespec = "seconds")
    line = f"{title.upper()}: {desc} ({timestamp})\n"

    try:
        with open(LOG_NAME, "x", encoding = "utf-8") as conn:
            conn.write(line)
    except FileExistsError:
        try:
            with open(LOG_NAME, "a", encoding = "utf-8") as conn:
                conn.write(line)
        except OSError as e:
            print(f"Unable to update the log ({e})")
    except OSError as e:
        print(f"Unable to create the log ({e})")
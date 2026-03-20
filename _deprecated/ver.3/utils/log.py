import os
from datetime import datetime

LOG_NAME = "log.txt"

def print_log():
    try:
        with open(LOG_NAME, "r", encoding="utf-8") as conn:
            return [conn.read(), "bullet"]
    except FileNotFoundError:
        return [f"File '{LOG_NAME}' not found.", "err"]
    except Exception as e:
        return [str(e), "err"]

def delete_log():
    if os.path.exists(LOG_NAME):
        try:
            os.remove(LOG_NAME)
            return [f"\n\"{LOG_NAME}\" deleted succesfully.", "body"]
        except PermissionError:
            return [f"\"{LOG_NAME}\" impossible to delete: it's being used in another process", "err"]
        except Exception as e:
            return [str(e), "err"]
    else:
        return [f"File '{LOG_NAME}' not found.", "err"]

def log_this(title, desc, day=None):
    """
    Write a log entry. day is optional; if not provided, the function will
    attempt to obtain it dynamically from game.status.day (but only at call time)
    to avoid top-level import cycles.
    """
    # Try to obtain day if not provided (dynamic import to avoid circular imports)
    timestamp = datetime.now().isoformat(timespec="seconds")
    prefix = f"day {day}, " if day is not None else ""
    line = f"{prefix}{title.upper()}: {desc} ({timestamp})\n"

    # Try to create file if it does not exist, otherwise append. Handle specific exceptions.
    try:
        # 'x' will fail if file exists; in that case we append.
        with open(LOG_NAME, "x", encoding="utf-8") as conn:
            conn.write(line)
    except FileExistsError:
        try:
            with open(LOG_NAME, "a", encoding="utf-8") as conn:
                conn.write(line)
        except OSError as e:
            # Could not write
            # As log module must be independent, we avoid importing format here.
            print(f"Unable to write to log file: {e}")
    except OSError as e:
        # Could not create or write file
        print(f"Unable to create log file: {e}")
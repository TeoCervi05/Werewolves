#there is a possibility to convert this simple script in a library (it will be necessary to remove the data import)
import os
from datetime import datetime
import data

LOG_NAME = "log.txt"

def print_log():
    try:
        with open(LOG_NAME) as conn:
            return [conn.read(), "bull"]
    except Exception as e:
            return[e, "err"]

def delete_log():
    if os.path.exists(LOG_NAME):
        try:
            os.remove(LOG_NAME)
            return [f"\n\"{LOG_NAME}\" deleted succesfully.", "body"]
        except PermissionError:
            return [f"\"{LOG_NAME}\" impossible to delete: it's being used in another process", "err"]
        except Exception as e:
            return [e, "err"]
    
    else:
        return [f"File '{LOG_NAME}' not found.", "err"]

def log_this(title, desc):
    try:
        with open(LOG_NAME, "x") as conn:
            conn.write(f"day {game.status.day}, {title.upper()}: {desc} ({datetime.now().isoformat()})")
    except:
        with open(LOG_NAME, "a") as conn:
            conn.write(f"_day {game.status.day}, {title.upper()}: {desc} ({datetime.now().isoformat()})")

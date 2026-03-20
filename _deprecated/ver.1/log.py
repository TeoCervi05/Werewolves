from datetime import datetime
from db import execute_commit, fetch_all

def log_this(day, title, desc):
    execute_commit(
        "INSERT INTO log (day, type, desc, phasestamp) VALUES (?, ?, ?, ?)",
        (day, title, desc, datetime.now().isoformat())
    )

def print_log():
    logs = fetch_all("SELECT * FROM log ORDER BY id ASC")
    print("\n--- GAME LOG ---")
    for log in logs:
        print(f" [{log['id']}] day {log['day']}, {log['type']}: {log['desc']} ({log['phasestamp']})")
    print()

def purge_log():
    execute_commit("DELETE FROM log")

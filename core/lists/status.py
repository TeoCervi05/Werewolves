from data.db import fetch_one, execute_commit
from utils.format import printf

def pull():
    # Ensure a status row exists and return (day, phase, turn).
    row = fetch_one("SELECT day FROM status WHERE id = 1")
    if not row:
        # Insert a full default row to avoid NULL fields.
        execute_commit("INSERT INTO status (day, phase, turn) VALUES (?, ?, ?)", (0, "setup", "master"))
    return fetch_one("SELECT day, phase, turn FROM status WHERE id = 1")

class Status:
    def __init__(self):
        data = pull()
        self.day = data[0]
        self.phase = data[1]
        self.turn = data[2]

    def show(self):
        printf("current status:", "head")
        printf(f"Day = {self.day};_Phase = {self.phase};_Turn = {self.turn}.", "bull")
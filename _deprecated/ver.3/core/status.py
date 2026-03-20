from data.db import fetch_one, execute_commit
from utils.format import prints

def pull_status():
    # Ensure a status row exists and return (day, phase, turn).
    row = fetch_one("SELECT day FROM status WHERE id = 1")
    if not row:
        # Insert a full default row to avoid NULL fields.
        execute_commit("INSERT INTO status (day, phase, turn) VALUES (?, ?, ?)", (0, "setup", "master"))
    return fetch_one("SELECT day, phase, turn FROM status WHERE id = 1")

class Status:
    def __init__(self):
        data = pull_status()
        self.day = data[0]
        self.phase = data[1]
        self.turn = data[2]

    def push(self):
        execute_commit(
            "UPDATE status SET day = ?, phase = ?, turn = ? WHERE id = 1",
            (self.day, self.phase, self.turn)
        )

    def show(self):
        prints("current status:", "head")
        prints(f"Day: {self.day}_Phase: {self.phase}_Turn: {self.turn}", "bullet")
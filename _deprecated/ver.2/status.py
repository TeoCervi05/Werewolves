from db import *
from format import prints

def pull():
    if not fetch_one("SELECT day FROM status WHERE id = 1"):
        execute_commit("INSERT INTO status (day) VALUES (0)")

    return fetch_one("SELECT day, phase, turn FROM status WHERE id = 1")

class Status:
    def __init__(self):
        data = pull()
        self.day = data[0]
        self.phase = data[1]
        self.turn = data[2]

    def push(self):
        execute_commit("UPDATE status SET day = ?, phase = ?, turn = ? WHERE id = ?", (self.day, self.phase, self.turn, 1))

    def show(self):
        prints("current status:", "head")
        prints(f"Day: {self.day}_Phase: {self.phase}_Turn: {self.turn}", "bull")
import sqlite3
import os
from log import log_this
from format import prints

DB_NAME = "game.db"

#connect to database
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

#create database if doesn't exists
def setup_database():
    with get_connection() as conn:
        cur = conn.cursor()

    #QUICK DATABASE LEGEND:
    #players, stores the variables for each players:
    #   name: name of the player;
    #   role: character interpreted during the game;
    #   soul: can be "white", "black";
    #   faction: can be "village", "wolves", "vampires" or "opponent";
    #   active: used by one-phase active power, or by "hidden" characters;
    #   romeo: true if he's been chosen by Juliet; 
    #   alive: true if he's still in game.
    #status, stores global game variables:
    #   day: current day;
    #   phase: can be "day", "voting", "ballot" or "night";
    #   turn: whose character is the current turn.

        cur.executescript("""
            CREATE TABLE IF NOT EXISTS status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day INTEGER DEFAULT 0,
                phase TEXT DEFAULT setup,
                turn TEXT DEFAULT master
            );

            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                role TEXT,
                soul TEXT,
                faction TEXT,
                active INTEGER DEFAULT 0,
                romeo INTEGER DEFAULT 0,
                alive INTEGER DEFAULT 1
            );
            """)

# delete database if the game session is over
def delete_database():
    if os.path.exists(DB_NAME):
        try:
            os.remove(DB_NAME)
            prints(f"\"{DB_NAME}\" deleted succesfully!", "body")
        except PermissionError:
            prints(f"\"{DB_NAME}\" impossible to delete: it's being used in another process", "err")
        except Exception as e:
            prints(e, "err")
    
    else:
        prints(f"Database '{DB_NAME}' not found.", "err")

# -- SEEK AND EXECUTE UTILITIES

def fetch_one(query, params=()):
    with get_connection() as conn:
        cur = conn.execute(query, params)
        return cur.fetchone()

def fetch_all(query, params=()):
    with get_connection() as conn:
        cur = conn.execute(query, params)
        return cur.fetchall()

def execute_commit(query, params=()):
    with get_connection() as conn:
        conn.execute(query, params)

#def setup_database():
#    with get_connection() as conn:
#        cur = conn.cursor()
#        cur.executescript("""
#        CREATE TABLE IF NOT EXISTS day (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            value INTEGER DEFAULT 0
#        );

#        CREATE TABLE IF NOT EXISTS players (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            name TEXT UNIQUE,
#            role TEXT,
#            soul TEXT,
#            faction TEXT,
#            active INTEGER DEFAULT 0,
#            romeo INTEGER DEFAULT 0,
#            alive INTEGER DEFAULT 1
#        );

#        CREATE TABLE IF NOT EXISTS log (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            day INTEGER,
#            type TEXT,
#            desc TEXT,
#            phasestamp TEXT
#        );


#        CREATE TABLE IF NOT EXISTS deathlist (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            name TEXT
#        );

#        CREATE TABLE IF NOT EXISTS votes (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            name TEXT,
#            votes INTEGER DEFAULT 0
#        );
#        """)
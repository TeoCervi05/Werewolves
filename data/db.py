import sqlite3
import os
from utils.log import log_this
from utils.format import printf

DB_NAME = "data/game.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    with get_connection() as conn:
        cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER DEFAULT 0,
            phase TEXT DEFAULT 'setup',
            turn TEXT DEFAULT 'master'
        );

        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            role TEXT,
            soul TEXT,
            faction TEXT,
            active INTEGER,
            romeo INTEGER DEFAULT 0,
            alive INTEGER DEFAULT 1
        );
    """)
    log_this("system", "backup database loaded")

#database purging (when asked)

def delete_db():
    #ADD LOGGING
    if os.path.exists(DB_NAME):
        try:
            os.remove(DB_NAME)
            printf(f"\"{DB_NAME}\" deleted succesfully!", "body")
        except PermissionError:
            printf(f"\"{DB_NAME}\" impossible to delete: it's being used in another process", "err")
        except Exception as e:
            printf(e, "err")
    
    else:
        printf(f"Database '{DB_NAME}' not found.", "err")

# -- SEEK AND EXECUTE UTILITIES

def fetch_one(query, params = ()):
    with get_connection() as conn:
        cur = conn.execute(query, params)
        return cur.fetchone()

def fetch_all(query, params = ()):
    with get_connection() as conn:
        cur = conn.execute(query, params)
        return cur.fetchall()

def execute_commit(query, params = ()):
    with get_connection() as conn:
        conn.execute(query, params)
import sqlite3

DB_NAME = "game.db"

def get_connection():
    #Connection to SQLite.
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    #Create tables if they doesn't exists
    with get_connection() as conn:
        cur = conn.cursor()
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS day (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER DEFAULT 0
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

        CREATE TABLE IF NOT EXISTS log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER,
            type TEXT,
            desc TEXT,
            phasestamp TEXT
        );

        CREATE TABLE IF NOT EXISTS deathlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );

        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            votes INTEGER DEFAULT 0
        );
        """)

# Helper SQL
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

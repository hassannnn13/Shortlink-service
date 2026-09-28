import sqlite3

def get_db(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str):
    conn = get_db(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS links (
            code TEXT PRIMARY KEY,
            url TEXT NOT NULL UNIQUE,
            clicks INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

import sqlite3

conn = sqlite3.connect("message.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    username TEXT,
    content TEXT,
    score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

def save_message(user_id:str,username:str,content:str,score:int):
    cursor.execute("""
    INSERT INTO logs (user_id,username,content,score)
    VALUES(?,?,?,?)
    """,(user_id,username,content,score))
    
    conn.commit()


def get_avg_userscore(user_id:str):
    cursor.execute("""
    SELECT AVG(score) FROM logs WHERE user_id = ?
    """, (user_id,))
    return cursor.fetchone()[0]

    
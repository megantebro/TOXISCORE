import sqlite3

from MessageData import MessageData

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_stats (
    id_
)""")


conn.commit()
conn.close()

def save_messages(msgDatas:list[MessageData], scores: list):
    """
    messages: List[MessageData]
    scores: List[int]
    """

    conn = sqlite3.connect("message.db")
    cursor = conn.cursor()

    for i in range(len(scores)):
        cursor.execute("""
            INSERT INTO logs (user_id, username, content, score)
            VALUES (?, ?, ?, ?)
        """, (msgDatas[i].user.id, msgDatas[i].user.display_name, msgDatas[i].content, scores[i]))

    conn.commit()
    conn.close()



def get_avg_userscore(user_id:str):
    conn = sqlite3.connect("message.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT AVG(score) FROM logs WHERE user_id = ?
    """, (user_id,))

    score = cursor.fetchone()[0]
    conn.close()
    return score

def get_server_avg():
    conn = sqlite3.connect("message.db")
    cursor = conn.cursor()

    cursor.execute("SELECT AVG(score) FROM logs")
    avg = cursor.fetchone()[0] or 0

    conn.close()
    return avg

def get_server_stddev():
    conn = sqlite3.connect("message.db")
    cursor = conn.cursor()

    cursor.execute("SELECT score FROM logs")
    scores = [row[0] for row in cursor.fetchall()]

    if len(scores) <= 1:
        return 0

    conn.close()
    import statistics
    return statistics.pstdev(scores)


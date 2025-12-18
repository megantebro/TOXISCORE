import datetime
import sqlite3
import statistics
import time

from MessageData import MessageData



db_path = "./message.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    guild_id TEXT,
    username TEXT,
    content TEXT,
    score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")


conn.commit()
conn.close()

def save_messages(msgDatas:list[MessageData], scores: list):
    """
    messages: List[MessageData]
    scores: List[int]
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for i in range(len(scores)):
        cursor.execute("""
            INSERT INTO logs (user_id,guild_id, username, content, score)
            VALUES (?, ?, ?, ?, ?)
        """, (msgDatas[i].user.id,msgDatas[i].guild_id, msgDatas[i].user.display_name, msgDatas[i].content, scores[i]))

    conn.commit()
    conn.close()



def get_avg_userscore(user_id:int,guild_id:int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT AVG(score) FROM logs WHERE user_id = ? AND guild_id = ?
    """, (user_id,guild_id))

    score = cursor.fetchone()[0]
    conn.close()
    return score

def get_server_avg(guild_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT AVG(score) FROM logs WHERE guild_id = ?",(guild_id,))
    avg = cursor.fetchone()[0] or 0

    conn.close()
    return avg

def get_server_stddev(guild_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT score FROM logs WHERE guild_id = ?",(guild_id,))
    scores = [row[0] for row in cursor.fetchall()]

    if len(scores) <= 1:
        return 0
    conn.close()
    import statistics
    return statistics.pstdev(scores)
    
def get_avg_rank(limit,worst,guild_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if worst: worst = "DESC"
    else:
        worst = "ASC"

    cursor.execute(f"""
        SELECT user_id, AVG(score) AS avg_score
        FROM logs
        WHERE guild_id = ?
        GROUP BY user_id
        ORDER BY avg_score {worst}
        LIMIT ?
    """, (guild_id,limit))

    rows = cursor.fetchall()
    conn.close()
    return rows

def get_total_rank(limit,worst,guild_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if worst: worst = "DESC"
    else: worst = "ASC"

    cursor.execute(f"""
        SELECT user_id, SUM(score) as sum_score
        FROM logs
        WHERE guild_id = ?
        GROUP BY user_id
        ORDER BY sum_score {worst}
        LIMIT ?
    """,(guild_id,limit))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_today_stats(guild_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT score
        FROM logs
        WHERE guild_id = ? AND
        date(created_at) = date("now","localtime")
    """,(guild_id,))

    rows = cursor.fetchall()
    conn.close()
    today = {}

    scores = [row[0] for row in rows]
    if scores:
        today["avg_today"] = statistics.mean(scores)
    else:
        today["avg_today"] = 0

    today["date"] = datetime.date.today()
    return today

    


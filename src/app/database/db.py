import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'conversations.db')

def drop_messages_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS messages')
    conn.commit()
    conn.close()

def init_db(force_recreate=True):
    if force_recreate:
        drop_messages_table()
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            message TEXT NOT NULL,
            is_bot BOOLEAN NOT NULL,
            title TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_message(thread_id: str, user_id: str, message: str, is_bot: bool, title: str = None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO messages (thread_id, user_id, message, is_bot, title) VALUES (?, ?, ?, ?, ?)',
        (thread_id, user_id, message, is_bot, title)
    )
    conn.commit()
    conn.close()

def get_user_conversations(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cur = conn.cursor()
    
    cur.execute('''
        SELECT thread_id, message, is_bot, timestamp, 
               (SELECT title FROM messages WHERE thread_id = m.thread_id AND title IS NOT NULL LIMIT 1) as title
        FROM messages m
        WHERE user_id = ? 
        ORDER BY thread_id, timestamp
    ''', (user_id,))
    
    rows = cur.fetchall()
    conversations = {}
    
    for row in rows:
        thread_id = row['thread_id']
        if thread_id not in conversations:
            conversations[thread_id] = {
                'title': row['title'] or 'Sem título',
                'messages': []
            }
        conversations[thread_id]['messages'].append({
            'message': row['message'],
            'is_bot': bool(row['is_bot']),
            'timestamp': row['timestamp']
        })
    
    conn.close()
    return conversations

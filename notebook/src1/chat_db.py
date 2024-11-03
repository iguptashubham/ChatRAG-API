import os
import sqlite3

class InteractionDB:
    def __init__(self):
        self.conn = self.get_database_connection()
        self.create_table()

    def get_database_connection(self):
        path = 'interaction_history/interaction_history.db'
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        print('Connection Established')
        return self.conn

    def create_table(self):
        conn = self.conn
        table = '''CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            ai_response TEXT,
            user_input TEXT,
            model TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
        conn.execute(table)
        conn.commit()

    def index_data(self, session_id, ai_response, user_input, model):
        conn = self.conn
        query = '''INSERT INTO chat_history (session_id, ai_response, user_input, model)
                   VALUES (?, ?, ?, ?)'''
        conn.execute(query, (session_id, ai_response, user_input, model))
        conn.commit()
    
    def retrieve_chat(self, session_id):
        conn = self.conn
        cursor = conn.cursor()
        query = '''SELECT ai_response, user_input FROM chat_history WHERE session_id = ? ORDER BY created_at'''
        cursor.execute(query, (session_id,))
        messages = []
        for row in cursor.fetchall():
            messages.extend([
                {'role': 'human', 'content': row['user_input']},
                {'role': 'ai', 'content': row['ai_response']}
            ])
        return messages
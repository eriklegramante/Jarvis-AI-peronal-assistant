import sqlite3
import os

class JarvisBrain:
    def __init__(self, db_path="memory_store.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Cria as tabelas se não existirem."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Tabela para fatos sobre o usuário
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profile (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            # Tabela para histórico de mensagens simplificado
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def store_fact(self, key, value):
        """Guarda uma informação importante (ex: 'user_name', 'Legramante')."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO user_profile (key, value) VALUES (?, ?)", (key, value))
            conn.commit()

    def get_fact(self, key):
        """Recupera um fato guardado."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM user_profile WHERE key = ?", (key,))
            result = cursor.fetchone()
            return result[0] if result else None
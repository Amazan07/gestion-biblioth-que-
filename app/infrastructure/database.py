import sqlite3

DB_PATH = "library.db"

def get_connection():
    """Ouvre une connexion vers le fichier SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crée les tables des livres et des emprunts si elles n'existent pas encore."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Table des livres
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                is_available INTEGER DEFAULT 1
            )
        """)
        
        # Table des emprunts avec ID automatique
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                loan_date TEXT NOT NULL,
                FOREIGN KEY(book_id) REFERENCES books(id)
            )
        """)
        conn.commit()
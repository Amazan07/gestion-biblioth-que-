import sqlite3
from datetime import datetime
from app.entities.book import Book
from app.use_cases.library_repository import LibraryRepository

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

def create_book(book_id: int, title: str, author: str) -> Book:
    """Insère un tout nouveau livre dans la base SQLite."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (id, title, author, is_available) VALUES (?, ?, ?, 1)",
            (book_id, title, author)
        )
        conn.commit()
    return Book(id=book_id, title=title, author=author, is_available=True)

def get_book_by_id(book_id: int):
    """Recherche un livre par son ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        
        if row:
            is_avail = True if row["is_available"] == 1 else False
            return Book(
                id=row["id"],
                title=row["title"],
                author=row["author"],
                is_available=is_avail
            )
        return None

def update_book_availability(book_id: int, is_available: bool):
    """Met à jour le statut du livre dans la base SQLite."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE books SET is_available = ? WHERE id = ?", 
            (1 if is_available else 0, book_id)
        )
        conn.commit()

def save_loan(book_id: int, student_id: int) -> int:
    """Enregistre un emprunt en base de données et retourne l'ID généré automatiquement."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO loans (book_id, student_id, loan_date) VALUES (?, ?, ?)",
            (book_id, student_id, datetime.now().isoformat())
        )
        conn.commit()
        return cursor.lastrowid


class SQLiteLibraryRepository(LibraryRepository):
    """Implémentation concrète de l'interface avec SQLite."""
    
    def get_book_by_id(self, book_id: int) -> Book:
        return get_book_by_id(book_id)

    def create_book(self, book_id: int, title: str, author: str) -> Book:
        return create_book(book_id, title, author)

    def update_book_availability(self, book_id: int, is_available: bool):
        return update_book_availability(book_id, is_available)

    def save_loan(self, book_id: int, student_id: int) -> int:
        return save_loan(book_id, student_id)
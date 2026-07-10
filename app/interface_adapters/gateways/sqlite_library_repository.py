import sqlite3
from datetime import datetime
from app.entities.book import Book
from app.use_cases.library_repository import LibraryRepository

DB_PATH = "library.db"

class SQLiteLibraryRepository(LibraryRepository):
    """Interface Adapter : Parle directement à la base de données SQLite."""
    
    def _get_connection(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def create_book(self, book_id: int, title: str, author: str) -> Book:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books (id, title, author, is_available) VALUES (?, ?, ?, 1)",
                (book_id, title, author)
            )
            conn.commit()
        return Book(id=book_id, title=title, author=author, is_available=True)

    def get_book_by_id(self, book_id: int) -> Book:
        with self._get_connection() as conn:
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

    def update_book_availability(self, book_id: int, is_available: bool):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE books SET is_available = ? WHERE id = ?", 
                (1 if is_available else 0, book_id)
            )
            conn.commit()

    def save_loan(self, book_id: int, student_id: int) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO loans (book_id, student_id, loan_date) VALUES (?, ?, ?)",
                (book_id, student_id, datetime.now().isoformat())
            )
            conn.commit()
            return cursor.lastrowid
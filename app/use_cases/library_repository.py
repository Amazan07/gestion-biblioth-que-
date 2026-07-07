from abc import ABC, abstractmethod
from app.entities.book import Book

class LibraryRepository(ABC):
    """Interface / Contrat abstrait pour l'accès aux données."""
    
    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Book:
        pass

    @abstractmethod
    def create_book(self, book_id: int, title: str, author: str) -> Book:
        pass

    @abstractmethod
    def update_book_availability(self, book_id: int, is_available: bool):
        pass

    @abstractmethod
    def save_loan(self, book_id: int, student_id: int) -> int:
        pass
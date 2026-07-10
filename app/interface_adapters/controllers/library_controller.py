from fastapi import HTTPException
from app.use_cases.borrow_book import BorrowBookUseCase
from app.use_cases.return_book import ReturnBookUseCase

class LibraryController:
    """Interface Adapter : Reçoit les requêtes de FastAPI et pilote les Use Cases."""
    
    def __init__(self, repository):
        self.borrow_use_case = BorrowBookUseCase(repository)
        self.return_use_case = ReturnBookUseCase(repository)
        self.repository = repository

    def add_book(self, id: int, title: str, author: str):
        try:
            from app.entities.book import Book
            validated_book = Book(id=id, title=title, author=author)
            self.repository.create_book(validated_book.id, validated_book.title, validated_book.author)
            return {"status": "success", "message": f"Book '{validated_book.title}' added successfully"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def borrow_book(self, book_id: int, student_id: int, student_name: str):
        result = self.borrow_use_case.execute(book_id, student_id, student_name)
        if not result.get("success", True):
            raise HTTPException(status_code=result.get("status_code", 400), detail=result.get("error"))
        return {"status": "success", "data": result}
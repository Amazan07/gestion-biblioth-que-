from app.entities.student import Student
from app.entities.loan import Loan
from app.use_cases.library_repository import LibraryRepository

class LibraryService:
    def __init__(self, repository: LibraryRepository):
        # On injecte l'interface
        self.repository = repository

    def borrow_book(self, book_id: int, student_id: int, student_name: str) -> dict:
        """Cas d'utilisation : Emprunter un livre de manière dynamique."""
        book = self.repository.get_book_by_id(book_id)
        if not book:
            return {"success": False, "error": "Livre non trouvé", "status_code": 404}
        
        if not book.is_available:
            return {"success": False, "error": f"Désolé, '{book.title}' est déjà emprunté", "status_code": 400}
        
        # 1. Enregistrement de l'emprunt dans l'infrastructure pour obtenir un ID unique
        generated_loan_id = self.repository.save_loan(book_id, student_id)
        
        # 2. Utilisation de nos entités pures avec les vraies valeurs dynamiques
        student = Student(id=student_id, name=student_name)
        loan = Loan(id=generated_loan_id, book_id=book.id, student_id=student.id)
        
        # 3. Mise à jour du statut du livre
        self.repository.update_book_availability(book_id, is_available=False)
        
        return {
            "success": True,
            "message": f"Le livre '{book.title}' (ID: {book.id}) a été emprunté avec succès par {student.name}.",
            "loan_details": {
                "loan_id": loan.id,
                "book_title": book.title,
                "book_id": loan.book_id,
                "student_id": loan.student_id
            }
        }

    def return_book(self, book_id: int) -> dict:
        """Cas d'utilisation : Rendre un livre."""
        book = self.repository.get_book_by_id(book_id)
        if not book:
            return {"success": False, "error": "Livre non trouvé", "status_code": 404}
        
        if book.is_available:
            return {"success": False, "error": "Ce livre est déjà présent dans la bibliothèque", "status_code": 400}
        
        self.repository.update_book_availability(book_id, is_available=True)
        
        return {
            "success": True,
            "message": f"Le livre '{book.title}' a bien été rendu et est à nouveau disponible."
        }
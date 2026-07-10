from app.use_cases.library_repository import LibraryRepository

class ReturnBookUseCase:
    def __init__(self, repository: LibraryRepository):
        self.repository = repository

    def execute(self, book_id: int) -> dict:
        """Exécute l'action de rendre un livre."""
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
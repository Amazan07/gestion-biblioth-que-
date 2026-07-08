class Book:
    def __init__(self, id: int, title: str, author: str, is_available: bool = True):
        
        if id <= 0:
            raise ValueError("L'ID du livre doit être un entier positif.")
        if not title.strip():
            raise ValueError("Le titre du livre ne peut pas être vide.")
        if not author.strip():
            raise ValueError("L'auteur du livre ne peut pas être vide.")

        self.id = id
        self.title = title
        self.author = author
        self.is_available = is_available

    
    def change_availability(self, status: bool):
        """Permet de modifier proprement le statut du livre."""
        self.is_available = status
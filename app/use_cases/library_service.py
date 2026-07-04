from datetime import datetime
from typing import Optional
from app.entities.book import Book
from app.entities.loan import Loan


class LibraryService:

    def __init__(self):
        # Pour ce mini-projet, on stocke les emprunts dans une liste en mémoire.
        # C'est simple, rapide et parfait pour valider l'architecture !
        self._loans = []

    def borrow_book(self, loan_id: int, book: Book, student_id: int) -> Optional[Loan]:
        """Cas d'utilisation : Emprunter un livre s'il est disponible"""
        # On vérifie si le livre est libre (Utilisation du @property id)
        if not book.is_available:
            print(f"Désolé, le livre '{book.title}' est déjà emprunté.")
            return None

        # 1. On change le statut du livre (Utilisation du @is_available.setter)
        book.is_available = False

        # 2. On crée l'objet Emprunt
        new_loan = Loan(
            id=loan_id,
            book_id=book.id,
            student_id=student_id,
            loan_date=datetime.now()
        )
        
        self._loans.append(new_loan)
        print(f"Succès ! Le livre '{book.title}' a été emprunté avec succès.")
        return new_loan

    def return_book(self, loan: Loan, book: Book):
        """Cas d'utilisation : Rendre un livre"""
        # 1. On remet le livre disponible
        book.is_available = True

        # 2. On enregistre la date de retour (Utilisation du @return_date.setter)
        loan.return_date = datetime.now()
        print(f"Le livre '{book.title}' a bien été retourné.")

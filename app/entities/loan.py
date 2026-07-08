from datetime import datetime, timedelta
from typing import Optional

class Loan:
    def __init__(self, id: int, book_id: int, student_id: int, loan_date: Optional[datetime] = None, return_date: Optional[datetime] = None):
        self.id = id
        self.book_id = book_id
        self.student_id = student_id
        self.loan_date = loan_date or datetime.now()
        self.return_date = return_date

    
    def get_due_date(self) -> datetime:
        """Calcule la date maximale de retour (J + 14 jours)."""
        return self.loan_date + timedelta(days=14)

    def is_overdue(self) -> bool:
        """Vérifie si l'emprunt a dépassé la date limite."""
        if self.return_date:
            return self.return_date > self.get_due_date()
        return datetime.now() > self.get_due_date()
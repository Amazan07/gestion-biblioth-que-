from datetime import datetime
from typing import Optional

class Loan:
    def __init__(self, id: Optional[int], book_id: int, student_id: int, loan_date: datetime, return_date: Optional[datetime] = None):
        # Attributs privés
        self._id = id
        self._book_id = book_id
        self._student_id = student_id
        self._loan_date = loan_date
        self._return_date = return_date

    # Getters pour lire les informations
    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def book_id(self) -> int:
        return self._book_id

    @property
    def student_id(self) -> int:
        return self._student_id

    @property
    def loan_date(self) -> datetime:
        return self._loan_date

    @property
    def return_date(self) -> Optional[datetime]:
        return self._return_date

    # Setter pour mettre à jour la date quand le livre est rendu
    @return_date.setter
    def return_date(self, date: Optional[datetime]):
        self._return_date = date

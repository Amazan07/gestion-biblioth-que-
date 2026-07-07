from datetime import datetime
from typing import Optional

class Loan:
    def __init__(self, id: int, book_id: int, student_id: int, loan_date: Optional[datetime] = None, return_date: Optional[datetime] = None):
        self.id = id
        self.book_id = book_id
        self.student_id = student_id
        self.loan_date = loan_date or datetime.now()
        self.return_date = return_date
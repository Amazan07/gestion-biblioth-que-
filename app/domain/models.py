from datetime import datetime
from typing import Optional


class Book:

    def __init__(
        self, 
        id: Optional[int], 
        title: str, 
        author: str, 
        isbn: str, 
        is_available: bool = True
    ):
        self.id = id                    
        self.title = title              
        self.author = author            
        self.isbn = isbn                
        self.is_available = is_available 


class Student:

    def __init__(
        self, 
        id: Optional[int], 
        name: str, 
        email: str
    ):
        self.id = id                    
        self.name = name                
        self.email = email              


class Loan:

    def __init__(
        self, 
        id: Optional[int], 
        book_id: int, 
        student_id: int, 
        loan_date: datetime, 
        return_date: Optional[datetime] = None
    ):
        self.id = id                    
        self.book_id = book_id          
        self.student_id = student_id    
        self.loan_date = loan_date      
        self.return_date = return_date  

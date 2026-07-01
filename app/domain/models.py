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
        # Attributs privés
        self.__id = id                    
        self.__title = title              
        self.__author = author            
        self.__isbn = isbn                
        self.__is_available = is_available 

    # Getters (Accesseurs) pour lire les informations en toute sécurité
    @property
    def id(self) -> Optional[int]:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def author(self) -> str:
        return self.__author

    @property
    def isbn(self) -> str:
        return self.__isbn

    @property
    def is_available(self) -> bool:
        return self.__is_available

    # Setters (Mutateurs) uniquement pour ce qui a besoin d'être modifié
    @is_available.setter
    def is_available(self, status: bool):
        self.__is_available = status


class Student:

    def __init__(
        self, 
        id: Optional[int], 
        name: str, 
        email: str
    ):
        # Attributs privés
        self.__id = id                    
        self.__name = name                
        self.__email = email              

    @property
    def id(self) -> Optional[int]:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email


class Loan:

    def __init__(
        self, 
        id: Optional[int], 
        book_id: int, 
        student_id: int, 
        loan_date: datetime, 
        return_date: Optional[datetime] = None
    ):
        # Attributs privés
        self.__id = id                    
        self.__book_id = book_id          
        self.__student_id = student_id    
        self.__loan_date = loan_date      
        self.__return_date = return_date  

    @property
    def id(self) -> Optional[int]:
        return self.__id

    @property
    def book_id(self) -> int:
        return self.__book_id

    @property
    def student_id(self) -> int:
        return self.__student_id

    @property
    def loan_date(self) -> datetime:
        return self.__loan_date

    @property
    def return_date(self) -> Optional[datetime]:
        return self.__return_date

    @return_date.setter
    def return_date(self, date: Optional[datetime]):
        self.__return_date = date

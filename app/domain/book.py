from typing import Optional

class Book:
    def __init__(self, id: Optional[int], title: str, author: str, isbn: str, is_available: bool = True):
        # Attributs privés (encapsulation simple)
        self._id = id
        self._title = title
        self._author = author
        self._isbn = isbn
        self._is_available = is_available

    # Getters simples pour lire les informations
    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def is_available(self) -> bool:
        return self._is_available

    # Setter simple pour modifier la disponibilité (quand on emprunte/rend)
    @is_available.setter
    def is_available(self, status: bool):
        self._is_available = status

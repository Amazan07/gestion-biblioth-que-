from typing import Optional

class Book:
    def __init__(self, id: int, title: str, is_available: bool = True):
        # Attributs privés
        self._id = id
        self._title = title
        self._is_available = is_available

    # Getter pour lire l'ID
    @property
    def id(self) -> int:
        return self._id

    # Getter pour lire le titre du livre
    @property
    def title(self) -> str:
        return self._title

    # Getter pour vérifier si le livre est disponible
    @property
    def is_available(self) -> bool:
        return self._is_available

    # Setter pour modifier la disponibilité du livre
    @is_available.setter
    def is_available(self, value: bool):
        self._is_available = value
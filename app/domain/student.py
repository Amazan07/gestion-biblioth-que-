from typing import Optional

class Student:
    def __init__(self, id: Optional[int], name: str, email: str):
        # Attributs privés
        self._id = id
        self._name = name
        self._email = email

    # Getters pour lire les informations
    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

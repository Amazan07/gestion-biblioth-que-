class Book:
    def __init__(self, id: int, title: str, author: str, is_available: bool = True):
        self.id = id
        self.title = title
        self.author = author
        self.is_available = is_available
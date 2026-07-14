from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Imports de tes adaptateurs et base de données
from app.interface_adapters.gateways.sqlite_library_repository import SQLiteLibraryRepository
from app.infrastructure.database import init_db

# Imports de tes cas d'utilisation (Use Cases)
from app.use_cases.borrow_book import BorrowBookUseCase
from app.use_cases.return_book import ReturnBookUseCase

# Initialisation de la base de données SQLite au démarrage
init_db()

app = FastAPI(
    title="Library Management System - Clean Architecture Strict",
    version="0.1.0"
)

# Modèle de données pour l'ajout de livre via l'API
class BookSchema(BaseModel):
    id: int
    title: str
    author: str

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de Gestion de Bibliothèque en Clean Architecture !"}

# 1. Route pour AJOUTER un livre
@app.post("/books", tags=["Books"])
def add_book(book: BookSchema):
    repository = SQLiteLibraryRepository()
    # Vérifier si le livre existe déjà
    existing_book = repository.get_book_by_id(book.id)
    if existing_book:
        raise HTTPException(status_code=400, detail="Ce livre existe déjà avec cet ID.")
    
    # Création du livre en base
    repository.save_book(book.id, book.title, book.author, is_available=True)
    return {"message": f"Le livre '{book.title}' a été ajouté avec succès !"}

# 2. Route pour EMPRUNTER un livre
@app.post("/borrow", tags=["Loans"])
def borrow_book(book_id: int):
    repository = SQLiteLibraryRepository()
    use_case = BorrowBookUseCase(repository)
    
    result = use_case.execute(book_id)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", 400), 
            detail=result.get("error")
        )
    
    return {"message": result.get("message")}

# 3. Route pour RENDRE un livre (La route manquante !)
@app.post("/return", tags=["Loans"])
def return_book(book_id: int):
    repository = SQLiteLibraryRepository()
    use_case = ReturnBookUseCase(repository)
    
    result = use_case.execute(book_id)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", 400), 
            detail=result.get("error")
        )
    
    return {"message": result.get("message")}
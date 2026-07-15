from fastapi import FastAPI, HTTPException

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

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de Gestion de Bibliothèque en Clean Architecture !"}

# 1. Route pour AJOUTER un livre (Corrigée avec create_book)
@app.post("/books", tags=["Books"])
def add_book(book_id: int, title: str, author: str):
    repository = SQLiteLibraryRepository()
    
    # Vérifier si le livre existe déjà
    existing_book = repository.get_book_by_id(book_id)
    if existing_book:
        raise HTTPException(status_code=400, detail="Ce livre existe déjà avec cet ID.")
    
    # Appel de la bonne méthode : create_book
    repository.create_book(book_id, title, author)
    return {"message": f"Le livre '{title}' a été ajouté avec succès !"}

# 2. Route pour EMPRUNTER un livre (Avec ID Livre, ID Étudiant, et Nom Étudiant !)
@app.post("/borrow", tags=["Loans"])
def borrow_book(book_id: int, student_id: int, student_name: str):
    repository = SQLiteLibraryRepository()
    use_case = BorrowBookUseCase(repository)
    
    # On passe bien les 3 paramètres attendus par ton Use Case : book_id, student_id, student_name
    result = use_case.execute(book_id, student_id, student_name)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=result.get("status_code", 400), 
            detail=result.get("error")
        )
    
    return {"message": result.get("message")}

# 3. Route pour RENDRE un livre
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
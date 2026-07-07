from fastapi import FastAPI, HTTPException
from app.use_cases.library_service import LibraryService
from app.infrastructure.database import SQLiteLibraryRepository
import app.infrastructure.database as db

app = FastAPI(title="Système de Gestion de Bibliothèque - Clean Architecture")

# Instanciation de l'infrastructure SQLite
repo_sqlite = SQLiteLibraryRepository()

# Injection de la dépendance dans le Use Case
service = LibraryService(repository=repo_sqlite)

@app.on_event("startup")
def startup_event():
    db.init_db()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API ! Rendez-vous sur /docs"}

@app.post("/books")
def add_book(book_id: int, title: str, author: str):
    existing_book = repo_sqlite.get_book_by_id(book_id)
    if existing_book:
        raise HTTPException(status_code=400, detail="Un livre avec cet ID existe déjà")
    
    new_book = repo_sqlite.create_book(book_id, title, author)
    return {
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author,
        "is_available": new_book.is_available
    }

@app.post("/borrow")
def borrow_book(book_id: int, student_id: int, student_name: str):
    result = service.borrow_book(book_id, student_id, student_name)
    if not result["success"]:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result

@app.post("/return")
def return_book(book_id: int):
    result = service.return_book(book_id)
    if not result["success"]:
        raise HTTPException(status_code=result["status_code"], detail=result["error"])
    return result
from fastapi import FastAPI, Form
from app.interface_adapters.gateways.sqlite_library_repository import SQLiteLibraryRepository
from app.interface_adapters.controllers.library_controller import LibraryController
from app.infrastructure.database import init_db 

app = FastAPI(title="Library Management System - Clean Architecture Strict")

# Instanciation de nos Interface Adapters
repository = SQLiteLibraryRepository()
controller = LibraryController(repository)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management API"}

@app.post("/books")
def add_book(id: int = Form(...), title: str = Form(...), author: str = Form(...)):
    return controller.add_book(id, title, author)

@app.post("/borrow")
def borrow_book(book_id: int = Form(...), student_id: int = Form(...), student_name: str = Form(...)):
    return controller.borrow_book(book_id, student_id, student_name)
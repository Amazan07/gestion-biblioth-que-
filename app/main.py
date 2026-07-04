from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.entities.book import Book
from app.use_cases.library_service import LibraryService

app = FastAPI(title="Gestion de Bibliothèque - Clean Architecture")
library_service = LibraryService()

# --- SIMULATION DE NOTRE BASE DE DONNÉES EN MÉMOIRE ---
# On crée un dictionnaire avec quelques livres de test pour l'exemple
fake_books_db = {
    1: Book(id=1, title="Le Petit Prince"),
    2: Book(id=2, title="Clean Architecture"),
    3: Book(id=3, title="Introduction à l'Informatique")
}

# --- MODELES POUR RECEVOIR LES DONNÉES (REQUEST BODIES) ---
class BorrowRequest(BaseModel):
    loan_id: int
    book_id: int
    student_id: int

@app.get("/books")
def list_books():
    # On récupère tous les objets Book de notre dictionnaire
    books_list = list(fake_books_db.values())
    
    # On structure une jolie réponse pour l'utilisateur
    result = []
    for book in books_list:
        result.append({
            "id": book.id,
            "title": book.title,
            "is_available": book.is_available
        })
        
    return {"books": result}

# --- ROUTES DE L'API ---

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de gestion de la bibliothèque !"}

@app.post("/borrow")
def borrow_book(request: BorrowRequest):
    # 1. On cherche si le livre existe dans notre fausse base de données
    book = fake_books_db.get(request.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    # 2. On appelle notre cas d'utilisation (Use Case)
    loan = library_service.borrow_book(
        loan_id=request.loan_id,
        book=book,
        student_id=request.student_id
    )
    
    # 3. Si le service renvoie None, c'est que le livre est déjà pris
    if not loan:
        raise HTTPException(status_code=400, detail=f"Le livre '{book.title}' est déjà emprunté.")
        
    return {
        "status": "success",
        "message": f"Le livre '{book.title}' a été emprunté avec succès.",
        "loan_id": loan.id
    }
# --- MODELE POUR RECEVOIR LES DONNÉES DE RETOUR ---
class ReturnRequest(BaseModel):
    book_id: int

@app.post("/return")
def return_book(request: ReturnRequest):
    # 1. On cherche si le livre existe dans notre fausse base de données
    book = fake_books_db.get(request.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    # 2. On va chercher l'emprunt actif pour ce livre dans notre service
    # On cherche dans la liste un emprunt qui correspond au book_id et qui n'a pas encore de date de retour
    active_loan = None
    for loan in library_service._loans:
        if loan.book_id == book.id and loan.return_date is None:
            active_loan = loan
            break
            
    if not active_loan:
        raise HTTPException(status_code=400, detail=f"Le livre '{book.title}' n'est pas marqué comme emprunté actuellement.")
    
    # 3. On appelle notre cas d'utilisation (Use Case) pour rendre le livre
    library_service.return_book(loan=active_loan, book=book)
    
    return {
        "status": "success",
        "message": f"Le livre '{book.title}' a bien été retourné et est de nouveau disponible."
    }

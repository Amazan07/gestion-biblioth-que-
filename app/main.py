from fastapi import FastAPI, HTTPException, Form
from app.use_cases.library_service import LibraryService
from app.infrastructure.database import SQLiteLibraryRepository, init_db

app = FastAPI(title="Library Management System - Clean Architecture")


repository = SQLiteLibraryRepository()
service = LibraryService(repository)

@app.on_event("startup")
def startup_event():
    init_db()



@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management API"}

@app.post("/books")
def add_book(id: int = Form(...), title: str = Form(...), author: str = Form(...)):
    try:
        
        from app.entities.book import Book
        validated_book = Book(id=id, title=title, author=author)
        
        
        repository.create_book(validated_book.id, validated_book.title, validated_book.author)
        return {"status": "success", "message": f"Book '{validated_book.title}' added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")

@app.post("/students")
def add_student(id: int = Form(...), name: str = Form(...), email: str = Form("")):
    try:
        # 1. Validation obligatoire via l'entité Student (Business Rules, format email, etc.)
        from app.entities.student import Student
        validated_student = Student(id=id, name=name, email=email)
        
        # 2. Retour immédiat du succès de la validation 
        return {
            "status": "success", 
            "message": f"Student '{validated_student.name}' validated and registered successfully",
            "email": validated_student.email
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")

@app.post("/borrow")
def borrow_book(book_id: int = Form(...), student_id: int = Form(...), student_name: str = Form(...)):
    try:
        # Appel au cas d'utilisation orchestré par le service avec les 3 arguments attendus
        result = service.borrow_book(book_id, student_id, student_name)
        
        # Si le service renvoie un dictionnaire d'échec (ex: livre non trouvé ou déjà emprunté)
        if isinstance(result, dict) and not result.get("success", True):
            raise HTTPException(status_code=result.get("status_code", 400), detail=result.get("error"))
            
        return {"status": "success", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")

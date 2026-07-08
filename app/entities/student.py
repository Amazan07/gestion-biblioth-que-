class Student:
    def __init__(self, id: int, name: str, email: str = ""):
        #  Validation du nom
        if not name.strip():
            raise ValueError("Le nom de l'étudiant ne peut pas être vide.")
            
       
        if email and ("@" not in email or "." not in email):
            raise ValueError("L'adresse email de l'étudiant n'est pas valide.")

        self.id = id
        self.name = name
        self.email = email
import os
from app.entities.book import Book
from app.interface_adapters.gateways.sqlite_library_repository import SQLiteLibraryRepository
from app.infrastructure.database import init_db
from app.use_cases.borrow_book import BorrowBookUseCase

print("=== DEBUT DU TEST TECHNIQUE ===")

# 1. On prépare la base de données de test locale
init_db()
repository = SQLiteLibraryRepository()

# 2. On s'assure d'avoir un livre de test propre dans la base (ID: 99)
# On nettoie d'abord si un vieux test traîne
with repository._get_connection() as conn:
    conn.execute("DELETE FROM books WHERE id = 99")
    conn.execute("DELETE FROM loans WHERE book_id = 99")
    conn.commit()

# On crée notre livre de test
repository.create_book(book_id=99, title="Clean Code", author="Robert C. Martin")
print("✅ Étape 1 : Livre de test inséré dans SQLite.")

# 3. ON INSTANCIE ET ON TESTE LE USE CASE
print("\n--- TEST DU USE CASE : BORROW BOOK ---")
borrow_use_case = BorrowBookUseCase(repository)

# Exécution du cas d'utilisation
resultat = borrow_use_case.execute(book_id=99, student_id=42, student_name="Dave")

# 4. VERIFICATION DU RESULTAT
if resultat.get("success") == True:
    print("✅ Succès : Le Use Case a validé et traité l'emprunt !")
    print(f"   Données retournées : {resultat}")
else:
    print(f"❌ Échec du Use Case : {resultat.get('error')}")

# 5. Deuxième tentative pour vérifier que le Use Case bloque si le livre est déjà pris
print("\n--- TEST DE SECURITE : Emprunter le même livre déjà pris ---")
resultat_bloque = borrow_use_case.execute(book_id=99, student_id=42, student_name="Dave")

if resultat_bloque.get("success") == False:
    print(f"✅ Succès du test : Le Use Case a bien refusé l'emprunt ! Message : '{resultat_bloque.get('error')}'")
else:
    print("❌ Échec : Le Use Case aurait dû bloquer cet emprunt.")

print("\n=== FIN DU TEST TECHNIQUE ===")
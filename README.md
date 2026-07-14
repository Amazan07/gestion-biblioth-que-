#  Système de Gestion de Bibliothèque — Clean Architecture

Ce projet est une application de gestion de bibliothèque construite avec **FastAPI** et **SQLite**, entièrement conçue selon les principes de la **Clean Architecture** (Architecture Propre). 

L'objectif de cette architecture est de séparer strictement la logique métier des détails technologiques (framework web, base de données).

---

##  Structure du Projet

L'arborescence respecte la séparation en couches préconisée par l'architecture :

```text
gestion-biblioth-que/
├── app/
│   ├── main.py                          # Point d'entrée de l'application (Framework FastAPI)
│   ├── entities/                        # Couche Entreprise (Cœur métier pur)
│   │   ├── book.py
│   │   └── student.py
│   ├── use_cases/                       # Couche Application (Scénarios d'utilisation)
│   │   ├── borrow_book.py
│   │   └── return_book.py
│   ├── interface_adapters/              # Couche Adaptateurs (Ponts technologiques)
│   │   ├── controllers/
│   │   │   └── library_controller.py    # Contrôle les flux d'entrée/sortie de l'API
│   │   └── gateways/
│   │       └── sqlite_library_repository.py # Parle directement à la base SQLite
│   └── infrastructure/                  # Couche Outils & Drivers (Détails techniques)
│       └── database.py                  # Initialisation et schémas de la base de données
├── test_entities.py                     # Script de test unitaire et technique autonome
├── .gitignore                           # Fichiers ignorés par Git (ex: library.db)
└── README.md

Installation et Lancement
1. Activer l'environnement virtuel
Sous Windows (PowerShell) : .venv\Scripts\Activate.ps1

2. Démarrer le serveur
Lancez le serveur Uvicorn depuis la racine du projet : uvicorn app.main:app --reload

Note : Au tout premier démarrage, le script de démarrage détecte l'absence de base de données locale et crée automatiquement le fichier library.db avec toutes les tables requises (books, loans). Le fichier .db est volontairement exclu du dépôt (via le .gitignore) afin de garantir un environnement propre pour chaque déploiement.

 Protocoles de Tests (Validation de l'Architecture)
Pour valider le bon fonctionnement de l'application et la robustesse de l'architecture, deux protocoles de tests sont disponibles :

 Méthode 1 : Tests fonctionnels via l'API (Swagger)
Cette méthode permet de tester l'intégration complète de la chaîne (de l'interface web jusqu'à la base de données).

Ouvrez votre navigateur sur l'interface Swagger de FastAPI : http://127.0.0.1:8000/docs

Scénario d'intégration à dérouler :

Ajouter un livre (POST /books) : Créez un livre avec un ID (ex: 10), un titre et un auteur.

Emprunter le livre (POST /borrow) : Effectuez un emprunt avec l'ID 10. Le statut du livre passe à "indisponible".

Tester la sécurité métier : Tentez d'emprunter à nouveau ce même livre ID 10. L'API doit retourner une erreur 400 (Livre déjà emprunté). C'est le cas d'utilisation qui bloque l'action.

Rendre le livre (POST /return) : Effectuez le retour du livre pour le rendre à nouveau disponible.

 Méthode 2 : Tests unitaires de la logique métier (Script isolé)
Ce test prouve que le cœur métier de l'application (les Entités et les Use Cases) peut fonctionner de manière totalement autonome, sans dépendre d'un serveur Web (FastAPI).

Exécutez le script autonome à la racine : python test_entities.py

Ce que ce test vérifie en direct dans votre console :

La validation stricte des règles de gestion par les entités (ex: interdiction d'avoir un titre vide).

L'exécution de la logique métier du cas d'utilisation d'emprunt (BorrowBookUseCase).

La détection automatique et le blocage d'une double réservation par le Use Case.
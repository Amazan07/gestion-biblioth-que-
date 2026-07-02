## Gestion de Bibliothèque - Clean Architecture & FastAPI

Ce projet est un mini-projet d'études visant à implémenter un système de gestion de bibliothèque en suivant les principes de la **Clean Architecture**, avec le framework **FastAPI** et **Python**.

## Structure Clean Architecture

Le projet respecte la séparation des préoccupations en couches distinctes. Les dépendances pointent uniquement vers l'intérieur (le Domaine ne dépend de rien).

```text
Utilisateur / Client (Navigateur Web)
      │
      ▼
┌───────────────┐
│   API Layer   │  <-- FastAPI (Routes, Requêtes HTTP)
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   Use Cases   │  <-- Logique Métier de l'application
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    Domain     │  <-- Entités pures (Book, Student, Loan) - COUCHE ACTUELLE
└───────────────┘
        ▲
        │
┌───────┴───────┐
│Infrastructure │  <-- Base de données(┘

 [ COUCHE EXTERNE (Infrastructure & API) ]      [ COUCHE INTERNE (Cœur Métier) ]
 
        app/api/ (FastAPI)
       ┌──────────────────┐
       │     routes.py    │─────┐
       └──────────────────┘     │
                                ▼
                       app/use_cases/                  app/domain/
                      ┌──────────────────┐            ┌──────────────────┐
                      │                  │            │     book.py      │
                      │ library_service  │───────────►├──────────────────┤
                      │       .py        │            │    student.py    │
                      │                  │            ├──────────────────┤
                      └──────────────────┘            │     loan.py      │
                                ▲                     └──────────────────┘
                                │                              ▲
        app/infrastructure/     │                              │
       ┌──────────────────┐     │                              │
       │   database.py    │─────┘                              │
       │    (SQLite)      │────────────────────────────────────┘
       └──────────────────┘

 gestion-biblioth-que-

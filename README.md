# HomeBudget
Simple Home Budget application

## Features
• user authentication (register, login)
• for simplicity, every user has a predefined X amount of money on their account
• categories CRUD
• expenses CRUD
• every bill is in relation with category
• filter bills by parameters (category, price min-max, date, and any other parameter you want)
• data aggregation endpoint (money earned & spent in last month, quarter, year, here you can play)


### Environment variables
Before starting the backend make sure you add the correct environment varialbe to be able to connect to the database.
For safely setting configuration settings like PostgreSQL connection information store those information on your OS 
either temporarily in the same terminal session as running the program or temporarily on your OS.

Example for temporarily for Windows:
$Env:DATABASE_ULR = "postgresql+psycopg2://username:password@localhost:5432/test_db"

## How to run

fastapi dev

docs available at http://127.0.0.1:8000/docs

## Technical Specification

For solving this task I used FastAPI as Python framework, PostgreSQL as Relational database and SQLAlchemy for ORM.

## Folder structure

app:
- `core/` -> application configuration and database engine setup
- `models/` -> SQLAlchemy ORM models
- `schemas/` -> Pydantic models used for request validation and response serialization
- `routers/` -> defines endpoints and delegates to services
- `services/` -> business logic layer
- `repositories/` -> all database queries
- `dependencies.py` -> shared FastAPI dependencies
- `main.py` -> application entry point

## Authentication and Authorization (WIP)

Authentication and Authorization will be implemented following OAuth2 specification.

### Authentication
Authentication will use password flow where user types username and password and in return his session gets back access token.
He then uses this token to send additional requests with this token in his Authorization header which confirms his identity and allows him to call APIs.

For password hashing pwdlib library is used with PasswordHash default options. 
It allows us to verify the password user enters with the hashed password in database which never gets exposed.

For password flow, JWT tokens will be used which hold the signature of the server, the format of the token and in the body some useful parameters like sub(username).
For signing the JWT token a random secret key was generated with the help of openssl.
The algorithm used to sign JWT token is HS256.

(maybe an authentication flow)

### Authorization (WIP)


## Database Schema

![schema.png](schema.png)


## Tests
For writing unit tests pytest framework will be used

## Database versioning
For versioning database Alembic is used.
Every time the any database model changes, Alembic recognizes it and suggest a SQL upgrade function to promote this new change into the real database.

## API versioning

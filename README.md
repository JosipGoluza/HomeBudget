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
- models ->
- routers -> 
- schemas -> 
- utils ->
- database_connection.py ->
- dependencies.py ->
- main.py -> 

## Authentication and Authorization (WIP)

Authentication and Authorization will be implemented following OAuth2 specification.

### Authentication
Authentication will use password flow where user types username and password and in return his session gets back access token.
He then uses this token to send additional requests with this token in his Authorization header which confirms his identity and allows him to call APIs.

(maybe an authentication flow)

### Authorization (WIP)


## Database Schema

![schema.png](schema.png)


## Tests
For writing unit tests pytest framework will be used
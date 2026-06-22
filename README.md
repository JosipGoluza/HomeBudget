# HomeBudget
Simple Home Budget application

## Features
• user authentication (register, login)
• for simplicity, every user has a predefined X amount of money on their account
• categories CRUD
• expenses CRUD
• every bill is in relation with category
• filter bills by parameters (category, price min-max, date, and any other parameter you want)
• data aggregation endpoint (money spent in last month, quarter, year, here you can play)


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

## Authentication

Authentication and Authorization will be implemented following OAuth2 specification.

### Authentication
Authentication will use password flow where user types username and password and in return his session gets back access token.
He then uses this token to send additional requests with this token in his Authorization header which confirms his identity and allows him to call APIs.

For password hashing pwdlib library is used with PasswordHash default options. 
It allows us to verify the password user enters with the hashed password in database which never gets exposed.

For password flow, JWT tokens will be used which hold the signature of the server, the format of the token and in the body some useful parameters like sub(username).
For signing the JWT token a random secret key was generated with the help of openssl.
The algorithm used to sign JWT token is HS256.


## Database Schema

![schema.png](schema.png)


## Tests
For writing unit tests pytest framework is used
run "pytest" command from terminal from root path to execute all tests

## Database versioning
For versioning database Alembic is used.
Every time any database model changes, Alembic recognizes it and suggest a SQL upgrade function to promote this new change into the real database.


## Database migration
When starting to do GET endpoint for categories, I realized that having predefined categories global for all users didn't have much sense.
Luckily I did not do much until that point so migrating from N : N to 1 : N (User <-> Category) was not that much painful.
I realized that later I would have more trouble because those predefined categories will not be editable and would be static for everyone.
Also, nobody would be able to delete those, and it is not worth to have N : N relationship just because of them.
The only downside is that each new user will create N new predefined categories for himself, but this downside is manageable against the above mentioned consequences.

This is what database looked like at that moment:

![schema_old.png](schema_old.png)

## Categories
User and Category are now related 1 : N because of the above mentioned reasons. Categories contains a foreign key pointing to the owner of the category and now he can edit and remove the default ones on his will.

There exists 5 Endpoints on the Categories resource, 4 CRUD ones for one category and one GET operation for fetching all categories a user has.

## Expenses
Expenses is related to both User and Category in N : 1 relation, user can have N expenses and they all belong to the one person and no one else. Same goes for category of the expense.

Other than 4 CRUD endpoints, expenses resource has 2 more endpoints. 

One is for fetching all of user's expenses but with these filters available as query parameters:
- category_id
- amount_min
- amount_max
- date_from
- date_to

The other is for generating a summary on his spendings where he can provide either Period (Enum) or a custom date (date_from and date_to)
- If he provides Period it can either be last "week" "month", "quarter" or "year" all as enum values
- If he provides a custom date range, then he will get all expenses that were entered in this time period
- He can also provide category_id if he wants to do summary on one of the categories.


## Balance
User can have predefined balance on his account. Every time he adds and expense he gets that value deducted from his balance. 

He cannot enter in the expense that is more than his current balanse as that would put him in the negative balance and we cannot allow him that.
On deletion of expense, his balance tops-up that same value.

When an expense amount is updated, the balance is re-settled by the difference between the new and old amount. If the increase would push the balance below zero, the update is rejected with the same not enough balance error as on creation.

Balance and expense amount values were migrated from Float to Numeric(12,2) because the float would cause a rounding error when summing numbers (eg. 49.99 + 20 = 69.99000000000001)

### Old reasoning for N : N relation
User and Category are related to Many-to-Many relation (N:N) where new user_categories_xref table is created holding their relationship.
For predefined categories, user_id value is null representing that no user owns them, but all other categories will set 
user_id to the value of the user who created them (you need to be authenticated to create your category).

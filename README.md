# HomeBudget

### Environment variables
Before starting the backend make sure you add the correct environment varialbe to be able to connect to the database.
For safely setting configuration settings like PostgreSQL connection information store those information on your OS 
either temporarily in the same terminal session as running the program or temporarily on your OS.

Example for temporarily for Windows:
$Env:DATABASE_ULR = "postgresql+psycopg2://username:password@localhost:5432/test_db"
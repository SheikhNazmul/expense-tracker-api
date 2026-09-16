from fastapi import FastAPI

from database import Base, engine
from router import auth, transactions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")
expensestrack = app

app.include_router(auth.router)
app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"message": "Expense Tracker API is running"}
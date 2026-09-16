from fastapi import FastAPI
from database import Base, engine
from router.auth import router as auth_router
from router.transactions import router as transaction_router

# Create tables in database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

# Include the routers
app.include_router(auth_router)
app.include_router(transaction_router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}
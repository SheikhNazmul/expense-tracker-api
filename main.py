import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from router.auth import router as auth_router
from router.transactions import router as transaction_router

# Create tables in database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

# Set FRONTEND_ORIGINS to a comma-separated list of deployed frontend origins.
origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include the routers
app.include_router(auth_router)
app.include_router(transaction_router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}

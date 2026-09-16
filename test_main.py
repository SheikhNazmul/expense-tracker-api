import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import date

from main import app
from database import Base, get_db

# Test database setup (SQLite in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite://"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=test_engine)

client = TestClient(app)

# Helper functions
def register_and_login(username: str = "testuser"):
    # Register
    register_data = {
        "username": username,
        "email": f"{username}@test.com",
        "password": "testpass123"
    }
    client.post("/auth/register", json=register_data)
    
    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "testpass123"
        }
    )
    return login_response.json()["access_token"]

def create_test_transaction(token: str):
    transaction_data = {
        "title": "Test Transaction",
        "amount": 100.0,
        "type": "expense",
        "category": "Food",
        "date": "2024-01-15"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/transactions/", json=transaction_data, headers=headers)
    return response.json()

# Test Cases
def test_create_transaction():
    token = register_and_login("createuser")
    headers = {"Authorization": f"Bearer {token}"}
    
    transaction_data = {
        "title": "Groceries",
        "amount": 50.5,
        "type": "expense",
        "category": "Food",
        "date": "2024-01-20"
    }
    
    response = client.post("/transactions/", json=transaction_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Groceries"
    assert data["amount"] == 50.5
    assert data["type"] == "expense"

def test_get_transactions():
    token = register_and_login("listuser")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a transaction first
    create_test_transaction(token)
    
    # Get all transactions
    response = client.get("/transactions/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_get_specific_transaction():
    token = register_and_login("specificuser")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create transaction
    transaction = create_test_transaction(token)
    transaction_id = transaction["id"]
    
    # Get specific transaction
    response = client.get(f"/transactions/{transaction_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction_id

def test_update_transaction():
    token = register_and_login("updateuser")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create transaction
    transaction = create_test_transaction(token)
    transaction_id = transaction["id"]
    
    # Update transaction
    update_data = {
        "title": "Updated Title",
        "amount": 200.0
    }
    response = client.put(f"/transactions/{transaction_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["amount"] == 200.0

def test_delete_transaction():
    token = register_and_login("deleteuser")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create transaction
    transaction = create_test_transaction(token)
    transaction_id = transaction["id"]
    
    # Delete transaction
    response = client.delete(f"/transactions/{transaction_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction deleted successfully"
    
    # Verify deletion
    response = client.get(f"/transactions/{transaction_id}", headers=headers)
    assert response.status_code == 404
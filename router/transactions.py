from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

# Notice the ".." to go up to the root folder
from database import get_db
from models import Transaction, User
from security import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])



router = APIRouter(prefix="/transactions", tags=["Transactions"])

class TransactionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0, description="Amount must be positive")
    type: str
    category: str = Field(..., min_length=1, max_length=50)
    date: date

class TransactionUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[str] = None
    category: Optional[str] = Field(default=None, min_length=1, max_length=50)
    date: Optional[date] = None

class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    type: str
    category: str
    date: date
    owner_id: int
    class Config:
        from_attributes = True

class Message(BaseModel):
    message: str

@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_transaction = Transaction(
        title=transaction.title,
        amount=transaction.amount,
        type=transaction.type,
        category=transaction.category,
        date=transaction.date,
        owner_id=current_user.id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=List[TransactionResponse])
def get_all_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Transaction).filter(Transaction.owner_id == current_user.id).all()

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.owner_id == current_user.id
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.owner_id == current_user.id
    ).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    update_data = transaction.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete("/{transaction_id}", response_model=Message)
def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.owner_id == current_user.id
    ).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}

@router.get("/filter", response_model=List[TransactionResponse])
def filter_transactions(
    type: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    minimum_amount: Optional[float] = Query(default=None, ge=0),
    maximum_amount: Optional[float] = Query(default=None, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction).filter(Transaction.owner_id == current_user.id)

    if type:
        query = query.filter(Transaction.type == type)
    if category:
        query = query.filter(Transaction.category == category)
    if minimum_amount is not None:
        query = query.filter(Transaction.amount >= minimum_amount)
    if maximum_amount is not None:
        query = query.filter(Transaction.amount <= maximum_amount)
    
    return query.all()
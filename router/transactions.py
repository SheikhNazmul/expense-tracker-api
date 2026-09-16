from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import models
import schemas
from database import get_db
from security import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=schemas.TransactionResponse, status_code=201)
def create_transaction(
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_transaction = models.Transaction(
        **transaction.model_dump(),
        owner_id=current_user.id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=List[schemas.TransactionResponse])
def get_all_transactions(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(models.Transaction).filter(
        models.Transaction.owner_id == current_user.id
    ).all()

@router.get("/filter", response_model=List[schemas.TransactionResponse])
def filter_transactions(
    type: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    minimum_amount: Optional[float] = Query(default=None, ge=0),
    maximum_amount: Optional[float] = Query(default=None, ge=0),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Transaction).filter(
        models.Transaction.owner_id == current_user.id
    )
    
    if type:
        query = query.filter(models.Transaction.type == type)
    if category:
        query = query.filter(models.Transaction.category == category)
    if minimum_amount is not None:
        query = query.filter(models.Transaction.amount >= minimum_amount)
    if maximum_amount is not None:
        query = query.filter(models.Transaction.amount <= maximum_amount)
    
    return query.all()

@router.get("/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(
    transaction_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.owner_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return transaction

@router.put("/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.owner_id == current_user.id
    ).first()
    
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    update_data = transaction.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete("/{transaction_id}", response_model=schemas.Message)
def delete_transaction(
    transaction_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.owner_id == current_user.id
    ).first()
    
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_transaction)
    db.commit()
    
    return {"message": "Transaction deleted successfully"}
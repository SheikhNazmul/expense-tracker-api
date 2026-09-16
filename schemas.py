from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import date

# User Schemas
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Transaction Schemas
class TransactionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0, description="Amount must be positive")
    type: Literal["income", "expense"]
    category: str = Field(..., min_length=1, max_length=50)
    date: date

class TransactionUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[Literal["income", "expense"]] = None
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

# Message Schema
class Message(BaseModel):
    message: str
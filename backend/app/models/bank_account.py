"""
Bank account model and schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class AccountType(str, Enum):
    """Bank account types"""
    SAVINGS = "Savings"
    CURRENT = "Current"
    SALARY = "Salary"


class BankAccountBase(BaseModel):
    """Base bank account schema"""
    bank_name: str = Field(..., min_length=2, max_length=100)
    account_number: str = Field(..., min_length=5, max_length=20)
    account_type: AccountType
    balance: float = Field(..., ge=0)
    currency: str = Field(default="INR")


class BankAccountCreate(BankAccountBase):
    """Bank account creation schema"""
    pass


class BankAccountUpdate(BaseModel):
    """Bank account update schema"""
    bank_name: Optional[str] = None
    account_type: Optional[AccountType] = None
    balance: Optional[float] = Field(None, ge=0)


class BankAccountResponse(BankAccountBase):
    """Bank account response schema"""
    id: str = Field(..., alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True

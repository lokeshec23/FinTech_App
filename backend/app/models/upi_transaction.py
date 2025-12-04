"""
UPI Transaction model and schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TransactionStatus(str, Enum):
    """Transaction status"""
    SUCCESS = "Success"
    FAILED = "Failed"
    PENDING = "Pending"


class UPITransactionBase(BaseModel):
    """Base UPI transaction schema"""
    transaction_id: str = Field(..., min_length=5, max_length=100)
    payee_name: str = Field(..., min_length=2, max_length=100)
    payee_upi: str = Field(..., min_length=5, max_length=100)
    amount: float = Field(..., gt=0)
    status: TransactionStatus = Field(default=TransactionStatus.SUCCESS)


class UPITransactionCreate(UPITransactionBase):
    """UPI transaction creation schema"""
    pass


class UPITransactionResponse(UPITransactionBase):
    """UPI transaction response schema"""
    id: str = Field(..., alias="_id")
    user_id: str
    timestamp: datetime
    created_at: datetime
    
    class Config:
        populate_by_name = True

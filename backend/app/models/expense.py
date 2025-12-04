"""
Expense model and schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ExpenseCategory(str, Enum):
    """Expense categories"""
    FOOD = "Food & Dining"
    TRANSPORT = "Transportation"
    UTILITIES = "Utilities"
    ENTERTAINMENT = "Entertainment"
    SHOPPING = "Shopping"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    RENT = "Rent"
    INSURANCE = "Insurance"
    INVESTMENTS = "Investments"
    OTHERS = "Others"


class PaymentMethod(str, Enum):
    """Payment methods"""
    CASH = "Cash"
    CARD = "Card"
    UPI = "UPI"
    NET_BANKING = "Net Banking"


class ExpenseBase(BaseModel):
    """Base expense schema"""
    category: ExpenseCategory
    amount: float = Field(..., gt=0)
    description: str = Field(..., min_length=1, max_length=500)
    date: datetime
    payment_method: PaymentMethod


class ExpenseCreate(ExpenseBase):
    """Expense creation schema"""
    pass


class ExpenseUpdate(BaseModel):
    """Expense update schema"""
    category: Optional[ExpenseCategory] = None
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    date: Optional[datetime] = None
    payment_method: Optional[PaymentMethod] = None


class ExpenseResponse(ExpenseBase):
    """Expense response schema"""
    id: str = Field(..., alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True

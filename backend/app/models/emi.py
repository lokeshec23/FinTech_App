"""
EMI (Equated Monthly Installment) model and schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum


class EMIStatus(str, Enum):
    """EMI status"""
    ACTIVE = "Active"
    COMPLETED = "Completed"
    DEFAULTED = "Defaulted"


class EMIBase(BaseModel):
    """Base EMI schema"""
    loan_name: str = Field(..., min_length=2, max_length=100)
    principal_amount: float = Field(..., gt=0)
    interest_rate: float = Field(..., ge=0, le=100)  # Annual interest rate in percentage
    tenure: int = Field(..., gt=0)  # Tenure in months
    start_date: date
    reminder_enabled: bool = Field(default=True)


class EMICreate(EMIBase):
    """EMI creation schema"""
    pass


class EMIUpdate(BaseModel):
    """EMI update schema"""
    loan_name: Optional[str] = Field(None, min_length=2, max_length=100)
    reminder_enabled: Optional[bool] = None
    status: Optional[EMIStatus] = None


class EMIResponse(EMIBase):
    """EMI response schema"""
    id: str = Field(..., alias="_id")
    user_id: str
    emi_amount: float
    next_payment_date: date
    remaining_tenure: int
    total_interest_paid: float
    principal_outstanding: float
    status: EMIStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True


class EMIPaymentSchedule(BaseModel):
    """EMI payment schedule item"""
    month: int
    payment_date: date
    emi_amount: float
    principal: float
    interest: float
    balance: float

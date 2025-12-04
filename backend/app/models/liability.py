"""
Liability model and schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum


class LiabilityType(str, Enum):
    """Liability types"""
    PERSONAL_LOAN = "Personal Loan"
    HOME_LOAN = "Home Loan"
    CAR_LOAN = "Car Loan"
    CREDIT_CARD = "Credit Card"
    EDUCATION_LOAN = "Education Loan"
    BUSINESS_LOAN = "Business Loan"
    OTHERS = "Others"


class LiabilityStatus(str, Enum):
    """Liability status"""
    ACTIVE = "Active"
    CLEARED = "Cleared"
    DEFAULTED = "Defaulted"


class LiabilityBase(BaseModel):
    """Base liability schema"""
    liability_type: LiabilityType
    name: str = Field(..., min_length=2, max_length=100)
    amount: float = Field(..., gt=0)
    interest_rate: Optional[float] = Field(None, ge=0, le=100)
    due_date: Optional[date] = None


class LiabilityCreate(LiabilityBase):
    """Liability creation schema"""
    pass


class LiabilityUpdate(BaseModel):
    """Liability update schema"""
    liability_type: Optional[LiabilityType] = None
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    amount: Optional[float] = Field(None, gt=0)
    interest_rate: Optional[float] = Field(None, ge=0, le=100)
    due_date: Optional[date] = None
    status: Optional[LiabilityStatus] = None


class LiabilityResponse(LiabilityBase):
    """Liability response schema"""
    id: str = Field(..., alias="_id")
    user_id: str
    status: LiabilityStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True

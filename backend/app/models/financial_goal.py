"""
Financial Goal model and schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum


class GoalStatus(str, Enum):
    """Goal status"""
    IN_PROGRESS = "In Progress"
    ACHIEVED = "Achieved"
    ABANDONED = "Abandoned"


class GoalCategory(str, Enum):
    """Goal categories"""
    SAVINGS = "Savings"
    INVESTMENT = "Investment"
    DEBT_REPAYMENT = "Debt Repayment"
    PURCHASE = "Purchase"
    EMERGENCY_FUND = "Emergency Fund"
    RETIREMENT = "Retirement"
    EDUCATION = "Education"
    OTHERS = "Others"


class FinancialGoalBase(BaseModel):
    """Base financial goal schema"""
    goal_name: str = Field(..., min_length=2, max_length=100)
    target_amount: float = Field(..., gt=0)
    current_amount: float = Field(default=0, ge=0)
    deadline: date
    category: GoalCategory


class FinancialGoalCreate(FinancialGoalBase):
    """Financial goal creation schema"""
    pass


class FinancialGoalUpdate(BaseModel):
    """Financial goal update schema"""
    goal_name: Optional[str] = Field(None, min_length=2, max_length=100)
    target_amount: Optional[float] = Field(None, gt=0)
    current_amount: Optional[float] = Field(None, ge=0)
    deadline: Optional[date] = None
    category: Optional[GoalCategory] = None
    status: Optional[GoalStatus] = None


class FinancialGoalResponse(FinancialGoalBase):
    """Financial goal response schema"""
    id: str = Field(..., alias="_id")
    user_id: str
    status: GoalStatus
    progress_percentage: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True

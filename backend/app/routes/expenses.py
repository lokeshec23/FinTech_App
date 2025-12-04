"""
Expense routes
"""
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from ..models.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from ..services.expense_service import ExpenseService
from ..utils.security import get_current_user_id

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=201)
async def create_expense(
    expense_data: ExpenseCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new expense"""
    service = ExpenseService()
    return await service.create_expense(user_id, expense_data)


@router.get("/", response_model=List[ExpenseResponse])
async def get_expenses(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2000),
    user_id: str = Depends(get_current_user_id)
):
    """Get all expenses, optionally filtered by month/year"""
    service = ExpenseService()
    return await service.get_expenses(user_id, month, year)


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get specific expense"""
    service = ExpenseService()
    return await service.get_expense_by_id(user_id, expense_id)


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: str,
    expense_update: ExpenseUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update expense"""
    service = ExpenseService()
    return await service.update_expense(user_id, expense_id, expense_update)


@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete expense"""
    service = ExpenseService()
    return await service.delete_expense(user_id, expense_id)

"""
Bank account routes
"""
from fastapi import APIRouter, Depends
from typing import List
from ..models.bank_account import BankAccountCreate, BankAccountUpdate, BankAccountResponse
from ..services.bank_account_service import BankAccountService
from ..utils.security import get_current_user_id

router = APIRouter(prefix="/api/bank-accounts", tags=["Bank Accounts"])


@router.post("/", response_model=BankAccountResponse, status_code=201)
async def create_account(
    account_data: BankAccountCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new bank account"""
    service = BankAccountService()
    return await service.create_account(user_id, account_data)


@router.get("/", response_model=List[BankAccountResponse])
async def get_accounts(user_id: str = Depends(get_current_user_id)):
    """Get all bank accounts"""
    service = BankAccountService()
    return await service.get_accounts(user_id)


@router.get("/total-balance")
async def get_total_balance(user_id: str = Depends(get_current_user_id)):
    """Get total balance across all accounts"""
    service = BankAccountService()
    total = await service.get_total_balance(user_id)
    return {"total_balance": total}


@router.get("/{account_id}", response_model=BankAccountResponse)
async def get_account(
    account_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get specific bank account"""
    service = BankAccountService()
    return await service.get_account_by_id(user_id, account_id)


@router.put("/{account_id}", response_model=BankAccountResponse)
async def update_account(
    account_id: str,
    account_update: BankAccountUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update bank account"""
    service = BankAccountService()
    return await service.update_account(user_id, account_id, account_update)


@router.delete("/{account_id}")
async def delete_account(
    account_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete bank account"""
    service = BankAccountService()
    return await service.delete_account(user_id, account_id)

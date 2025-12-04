"""
UPI transaction routes
"""
from fastapi import APIRouter, Depends
from typing import List
from ..models.upi_transaction import UPITransactionCreate, UPITransactionResponse
from ..services.upi_service import UPITransactionService
from ..utils.security import get_current_user_id

router = APIRouter(prefix="/api/upi", tags=["UPI Transactions"])


@router.post("/", response_model=UPITransactionResponse, status_code=201)
async def create_transaction(
    transaction_data: UPITransactionCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new UPI transaction"""
    service = UPITransactionService()
    return await service.create_transaction(user_id, transaction_data)


@router.get("/", response_model=List[UPITransactionResponse])
async def get_transactions(user_id: str = Depends(get_current_user_id)):
    """Get all UPI transactions"""
    service = UPITransactionService()
    return await service.get_transactions(user_id)


@router.get("/{transaction_id}", response_model=UPITransactionResponse)
async def get_transaction(
    transaction_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get specific UPI transaction"""
    service = UPITransactionService()
    return await service.get_transaction_by_id(user_id, transaction_id)


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete UPI transaction"""
    service = UPITransactionService()
    return await service.delete_transaction(user_id, transaction_id)

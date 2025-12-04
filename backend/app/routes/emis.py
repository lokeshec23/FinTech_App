"""
EMI routes
"""
from fastapi import APIRouter, Depends, Query
from typing import List
from ..models.emi import EMICreate, EMIUpdate, EMIResponse, EMIPaymentSchedule
from ..services.emi_service import EMIService
from ..utils.security import get_current_user_id

router = APIRouter(prefix="/api/emis", tags=["EMIs"])


@router.post("/", response_model=EMIResponse, status_code=201)
async def create_emi(
    emi_data: EMICreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new EMI"""
    service = EMIService()
    return await service.create_emi(user_id, emi_data)


@router.get("/", response_model=List[EMIResponse])
async def get_emis(user_id: str = Depends(get_current_user_id)):
    """Get all EMIs"""
    service = EMIService()
    return await service.get_emis(user_id)


@router.get("/upcoming", response_model=List[EMIResponse])
async def get_upcoming_payments(
    days: int = Query(7, ge=1, le=30),
    user_id: str = Depends(get_current_user_id)
):
    """Get EMIs with payments due in next N days"""
    service = EMIService()
    return await service.get_upcoming_payments(user_id, days)


@router.get("/{emi_id}", response_model=EMIResponse)
async def get_emi(
    emi_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get specific EMI"""
    service = EMIService()
    return await service.get_emi_by_id(user_id, emi_id)


@router.get("/{emi_id}/schedule", response_model=List[EMIPaymentSchedule])
async def get_payment_schedule(
    emi_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get payment schedule for an EMI"""
    service = EMIService()
    return await service.get_payment_schedule(user_id, emi_id)


@router.put("/{emi_id}", response_model=EMIResponse)
async def update_emi(
    emi_id: str,
    emi_update: EMIUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update EMI"""
    service = EMIService()
    return await service.update_emi(user_id, emi_id, emi_update)


@router.delete("/{emi_id}")
async def delete_emi(
    emi_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete EMI"""
    service = EMIService()
    return await service.delete_emi(user_id, emi_id)

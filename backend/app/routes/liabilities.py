"""
Liability routes
"""
from fastapi import APIRouter, Depends
from typing import List
from ..models.liability import LiabilityCreate, LiabilityUpdate, LiabilityResponse
from ..services.liability_service import LiabilityService
from ..utils.security import get_current_user_id

router = APIRouter(prefix="/api/liabilities", tags=["Liabilities"])


@router.post("/", response_model=LiabilityResponse, status_code=201)
async def create_liability(
    liability_data: LiabilityCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new liability"""
    service = LiabilityService()
    return await service.create_liability(user_id, liability_data)


@router.get("/", response_model=List[LiabilityResponse])
async def get_liabilities(user_id: str = Depends(get_current_user_id)):
    """Get all liabilities"""
    service = LiabilityService()
    return await service.get_liabilities(user_id)


@router.get("/{liability_id}", response_model=LiabilityResponse)
async def get_liability(
    liability_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get specific liability"""
    service = LiabilityService()
    return await service.get_liability_by_id(user_id, liability_id)


@router.put("/{liability_id}", response_model=LiabilityResponse)
async def update_liability(
    liability_id: str,
    liability_update: LiabilityUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update liability"""
    service = LiabilityService()
    return await service.update_liability(user_id, liability_id, liability_update)


@router.delete("/{liability_id}")
async def delete_liability(
    liability_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete liability"""
    service = LiabilityService()
    return await service.delete_liability(user_id, liability_id)

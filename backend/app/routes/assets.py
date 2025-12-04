"""
Asset routes
"""
from fastapi import APIRouter, Depends
from typing import List
from ..models.asset import AssetCreate, AssetUpdate, AssetResponse
from ..services.asset_service import AssetService
from ..utils.security import get_current_user_id

router = APIRouter(prefix="/api/assets", tags=["Assets"])


@router.post("/", response_model=AssetResponse, status_code=201)
async def create_asset(
    asset_data: AssetCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new asset"""
    service = AssetService()
    return await service.create_asset(user_id, asset_data)


@router.get("/", response_model=List[AssetResponse])
async def get_assets(user_id: str = Depends(get_current_user_id)):
    """Get all assets"""
    service = AssetService()
    return await service.get_assets(user_id)


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get specific asset"""
    service = AssetService()
    return await service.get_asset_by_id(user_id, asset_id)


@router.put("/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: str,
    asset_update: AssetUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update asset"""
    service = AssetService()
    return await service.update_asset(user_id, asset_id, asset_update)


@router.delete("/{asset_id}")
async def delete_asset(
    asset_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete asset"""
    service = AssetService()
    return await service.delete_asset(user_id, asset_id)

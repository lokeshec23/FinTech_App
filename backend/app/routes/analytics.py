"""
Analytics routes
"""
from fastapi import APIRouter, Depends
from typing import Dict, Any
from ..services.analytics_service import AnalyticsService
from ..utils.security import get_current_user_id

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard(user_id: str = Depends(get_current_user_id)):
    """Get complete dashboard summary"""
    service = AnalyticsService()
    return await service.get_dashboard_summary(user_id)

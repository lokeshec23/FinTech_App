"""
Financial goal routes
"""
from fastapi import APIRouter, Depends
from typing import List
from ..models.financial_goal import FinancialGoalCreate, FinancialGoalUpdate, FinancialGoalResponse
from ..services.goal_service import FinancialGoalService
from ..utils.security import get_current_user_id

router = APIRouter(prefix="/api/goals", tags=["Financial Goals"])


@router.post("/", response_model=FinancialGoalResponse, status_code=201)
async def create_goal(
    goal_data: FinancialGoalCreate,
    user_id: str = Depends(get_current_user_id)
):
    """Create a new financial goal"""
    service = FinancialGoalService()
    return await service.create_goal(user_id, goal_data)


@router.get("/", response_model=List[FinancialGoalResponse])
async def get_goals(user_id: str = Depends(get_current_user_id)):
    """Get all financial goals"""
    service = FinancialGoalService()
    return await service.get_goals(user_id)


@router.get("/{goal_id}", response_model=FinancialGoalResponse)
async def get_goal(
    goal_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Get specific financial goal"""
    service = FinancialGoalService()
    return await service.get_goal_by_id(user_id, goal_id)


@router.put("/{goal_id}", response_model=FinancialGoalResponse)
async def update_goal(
    goal_id: str,
    goal_update: FinancialGoalUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """Update financial goal"""
    service = FinancialGoalService()
    return await service.update_goal(user_id, goal_id, goal_update)


@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """Delete financial goal"""
    service = FinancialGoalService()
    return await service.delete_goal(user_id, goal_id)

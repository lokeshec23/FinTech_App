"""
Financial goal service
"""
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from typing import List
from ..models.financial_goal import FinancialGoalCreate, FinancialGoalUpdate, FinancialGoalResponse, GoalStatus
from ..database import get_database


class FinancialGoalService:
    """Financial goal management service"""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.financial_goals
    
    def _calculate_progress(self, current: float, target: float) -> float:
        """Calculate progress percentage"""
        if target == 0:
            return 0.0
        progress = (current / target) * 100
        return min(round(progress, 2), 100.0)
    
    async def create_goal(self, user_id: str, goal_data: FinancialGoalCreate) -> FinancialGoalResponse:
        """Create a new financial goal"""
        goal_dict = goal_data.dict()
        goal_dict["user_id"] = user_id
        goal_dict["status"] = GoalStatus.IN_PROGRESS
        goal_dict["progress_percentage"] = self._calculate_progress(
            goal_dict["current_amount"],
            goal_dict["target_amount"]
        )
        goal_dict["created_at"] = datetime.utcnow()
        goal_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(goal_dict)
        goal_dict["_id"] = str(result.inserted_id)
        
        return FinancialGoalResponse(**goal_dict, id=str(result.inserted_id))
    
    async def get_goals(self, user_id: str) -> List[FinancialGoalResponse]:
        """Get all financial goals for a user"""
        goals = []
        cursor = self.collection.find({"user_id": user_id})
        
        async for goal in cursor:
            goal["_id"] = str(goal["_id"])
            goals.append(FinancialGoalResponse(**goal, id=goal["_id"]))
        
        return goals
    
    async def get_goal_by_id(self, user_id: str, goal_id: str) -> FinancialGoalResponse:
        """Get specific financial goal"""
        goal = await self.collection.find_one({
            "_id": ObjectId(goal_id),
            "user_id": user_id
        })
        
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        
        return FinancialGoalResponse(**goal, id=str(goal["_id"]))
    
    async def update_goal(self, user_id: str, goal_id: str, 
                        goal_update: FinancialGoalUpdate) -> FinancialGoalResponse:
        """Update financial goal"""
        # Get current goal to recalculate progress
        current_goal = await self.get_goal_by_id(user_id, goal_id)
        
        update_data = {k: v for k, v in goal_update.dict().items() if v is not None}
        
        # Recalculate progress if amounts changed
        current_amount = update_data.get("current_amount", current_goal.current_amount)
        target_amount = update_data.get("target_amount", current_goal.target_amount)
        update_data["progress_percentage"] = self._calculate_progress(current_amount, target_amount)
        
        # Auto-update status if goal is achieved
        if update_data["progress_percentage"] >= 100:
            update_data["status"] = GoalStatus.ACHIEVED
        
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(goal_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        
        return FinancialGoalResponse(**result, id=str(result["_id"]))
    
    async def delete_goal(self, user_id: str, goal_id: str) -> dict:
        """Delete financial goal"""
        result = await self.collection.delete_one({
            "_id": ObjectId(goal_id),
            "user_id": user_id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        
        return {"message": "Goal deleted successfully"}

"""
Expense tracking service
"""
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from typing import List, Optional
from ..models.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from ..database import get_database


class ExpenseService:
    """Expense tracking service"""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.expenses
    
    async def create_expense(self, user_id: str, expense_data: ExpenseCreate) -> ExpenseResponse:
        """Create a new expense"""
        expense_dict = expense_data.dict()
        expense_dict["user_id"] = user_id
        expense_dict["created_at"] = datetime.utcnow()
        expense_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(expense_dict)
        expense_dict["_id"] = str(result.inserted_id)
        
        return ExpenseResponse(**expense_dict, id=str(result.inserted_id))
    
    async def get_expenses(self, user_id: str, month: Optional[int] = None, 
                          year: Optional[int] = None) -> List[ExpenseResponse]:
        """Get expenses for a user, optionally filtered by month/year"""
        query = {"user_id": user_id}
        
        # Add month/year filter if provided
        if month and year:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            
            query["date"] = {"$gte": start_date, "$lt": end_date}
        
        expenses = []
        cursor = self.collection.find(query).sort("date", -1)
        
        async for expense in cursor:
            expense["_id"] = str(expense["_id"])
            expenses.append(ExpenseResponse(**expense, id=expense["_id"]))
        
        return expenses
    
    async def get_expense_by_id(self, user_id: str, expense_id: str) -> ExpenseResponse:
        """Get specific expense"""
        expense = await self.collection.find_one({
            "_id": ObjectId(expense_id),
            "user_id": user_id
        })
        
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        
        return ExpenseResponse(**expense, id=str(expense["_id"]))
    
    async def update_expense(self, user_id: str, expense_id: str, 
                           expense_update: ExpenseUpdate) -> ExpenseResponse:
        """Update expense"""
        update_data = {k: v for k, v in expense_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(expense_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        
        return ExpenseResponse(**result, id=str(result["_id"]))
    
    async def delete_expense(self, user_id: str, expense_id: str) -> dict:
        """Delete expense"""
        result = await self.collection.delete_one({
            "_id": ObjectId(expense_id),
            "user_id": user_id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )
        
        return {"message": "Expense deleted successfully"}

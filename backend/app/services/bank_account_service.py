"""
Bank account service
"""
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from typing import List
from ..models.bank_account import BankAccountCreate, BankAccountUpdate, BankAccountResponse
from ..database import get_database


class BankAccountService:
    """Bank account management service"""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.bank_accounts
    
    async def create_account(self, user_id: str, account_data: BankAccountCreate) -> BankAccountResponse:
        """Create a new bank account"""
        account_dict = account_data.dict()
        account_dict["user_id"] = user_id
        account_dict["created_at"] = datetime.utcnow()
        account_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(account_dict)
        account_dict["_id"] = str(result.inserted_id)
        
        return BankAccountResponse(**account_dict, id=str(result.inserted_id))
    
    async def get_accounts(self, user_id: str) -> List[BankAccountResponse]:
        """Get all bank accounts for a user"""
        accounts = []
        cursor = self.collection.find({"user_id": user_id})
        
        async for account in cursor:
            account["_id"] = str(account["_id"])
            accounts.append(BankAccountResponse(**account, id=account["_id"]))
        
        return accounts
    
    async def get_account_by_id(self, user_id: str, account_id: str) -> BankAccountResponse:
        """Get specific bank account"""
        account = await self.collection.find_one({
            "_id": ObjectId(account_id),
            "user_id": user_id
        })
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bank account not found"
            )
        
        return BankAccountResponse(**account, id=str(account["_id"]))
    
    async def update_account(self, user_id: str, account_id: str, 
                           account_update: BankAccountUpdate) -> BankAccountResponse:
        """Update bank account"""
        update_data = {k: v for k, v in account_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(account_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bank account not found"
            )
        
        return BankAccountResponse(**result, id=str(result["_id"]))
    
    async def delete_account(self, user_id: str, account_id: str) -> dict:
        """Delete bank account"""
        result = await self.collection.delete_one({
            "_id": ObjectId(account_id),
            "user_id": user_id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bank account not found"
            )
        
        return {"message": "Bank account deleted successfully"}
    
    async def get_total_balance(self, user_id: str) -> float:
        """Get total balance across all accounts"""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": None, "total": {"$sum": "$balance"}}}
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0.0

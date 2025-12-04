"""
UPI transaction service
"""
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from typing import List
from ..models.upi_transaction import UPITransactionCreate, UPITransactionResponse
from ..database import get_database


class UPITransactionService:
    """UPI transaction management service"""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.upi_transactions
    
    async def create_transaction(self, user_id: str, transaction_data: UPITransactionCreate) -> UPITransactionResponse:
        """Create a new UPI transaction"""
        transaction_dict = transaction_data.dict()
        transaction_dict["user_id"] = user_id
        transaction_dict["timestamp"] = datetime.utcnow()
        transaction_dict["created_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(transaction_dict)
        transaction_dict["_id"] = str(result.inserted_id)
        
        return UPITransactionResponse(**transaction_dict, id=str(result.inserted_id))
    
    async def get_transactions(self, user_id: str) -> List[UPITransactionResponse]:
        """Get all UPI transactions for a user"""
        transactions = []
        cursor = self.collection.find({"user_id": user_id}).sort("timestamp", -1)
        
        async for transaction in cursor:
            transaction["_id"] = str(transaction["_id"])
            transactions.append(UPITransactionResponse(**transaction, id=transaction["_id"]))
        
        return transactions
    
    async def get_transaction_by_id(self, user_id: str, transaction_id: str) -> UPITransactionResponse:
        """Get specific UPI transaction"""
        transaction = await self.collection.find_one({
            "_id": ObjectId(transaction_id),
            "user_id": user_id
        })
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        return UPITransactionResponse(**transaction, id=str(transaction["_id"]))
    
    async def delete_transaction(self, user_id: str, transaction_id: str) -> dict:
        """Delete UPI transaction"""
        result = await self.collection.delete_one({
            "_id": ObjectId(transaction_id),
            "user_id": user_id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        return {"message": "Transaction deleted successfully"}

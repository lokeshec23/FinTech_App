"""
Liability service
"""
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from typing import List
from ..models.liability import LiabilityCreate, LiabilityUpdate, LiabilityResponse
from ..database import get_database


class LiabilityService:
    """Liability management service"""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.liabilities
    
    async def create_liability(self, user_id: str, liability_data: LiabilityCreate) -> LiabilityResponse:
        """Create a new liability"""
        liability_dict = liability_data.dict()
        liability_dict["user_id"] = user_id
        liability_dict["status"] = "Active"
        liability_dict["created_at"] = datetime.utcnow()
        liability_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(liability_dict)
        liability_dict["_id"] = str(result.inserted_id)
        
        return LiabilityResponse(**liability_dict, id=str(result.inserted_id))
    
    async def get_liabilities(self, user_id: str) -> List[LiabilityResponse]:
        """Get all liabilities for a user"""
        liabilities = []
        cursor = self.collection.find({"user_id": user_id})
        
        async for liability in cursor:
            liability["_id"] = str(liability["_id"])
            liabilities.append(LiabilityResponse(**liability, id=liability["_id"]))
        
        return liabilities
    
    async def get_liability_by_id(self, user_id: str, liability_id: str) -> LiabilityResponse:
        """Get specific liability"""
        liability = await self.collection.find_one({
            "_id": ObjectId(liability_id),
            "user_id": user_id
        })
        
        if not liability:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Liability not found"
            )
        
        return LiabilityResponse(**liability, id=str(liability["_id"]))
    
    async def update_liability(self, user_id: str, liability_id: str, 
                             liability_update: LiabilityUpdate) -> LiabilityResponse:
        """Update liability"""
        update_data = {k: v for k, v in liability_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(liability_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Liability not found"
            )
        
        return LiabilityResponse(**result, id=str(result["_id"]))
    
    async def delete_liability(self, user_id: str, liability_id: str) -> dict:
        """Delete liability"""
        result = await self.collection.delete_one({
            "_id": ObjectId(liability_id),
            "user_id": user_id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Liability not found"
            )
        
        return {"message": "Liability deleted successfully"}

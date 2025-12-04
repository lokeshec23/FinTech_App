"""
Asset service
"""
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from typing import List
from ..models.asset import AssetCreate, AssetUpdate, AssetResponse
from ..database import get_database


class AssetService:
    """Asset management service"""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.assets
    
    async def create_asset(self, user_id: str, asset_data: AssetCreate) -> AssetResponse:
        """Create a new asset"""
        asset_dict = asset_data.dict()
        asset_dict["user_id"] = user_id
        asset_dict["created_at"] = datetime.utcnow()
        asset_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(asset_dict)
        asset_dict["_id"] = str(result.inserted_id)
        
        return AssetResponse(**asset_dict, id=str(result.inserted_id))
    
    async def get_assets(self, user_id: str) -> List[AssetResponse]:
        """Get all assets for a user"""
        assets = []
        cursor = self.collection.find({"user_id": user_id})
        
        async for asset in cursor:
            asset["_id"] = str(asset["_id"])
            assets.append(AssetResponse(**asset, id=asset["_id"]))
        
        return assets
    
    async def get_asset_by_id(self, user_id: str, asset_id: str) -> AssetResponse:
        """Get specific asset"""
        asset = await self.collection.find_one({
            "_id": ObjectId(asset_id),
            "user_id": user_id
        })
        
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        
        return AssetResponse(**asset, id=str(asset["_id"]))
    
    async def update_asset(self, user_id: str, asset_id: str, 
                         asset_update: AssetUpdate) -> AssetResponse:
        """Update asset"""
        update_data = {k: v for k, v in asset_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(asset_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        
        return AssetResponse(**result, id=str(result["_id"]))
    
    async def delete_asset(self, user_id: str, asset_id: str) -> dict:
        """Delete asset"""
        result = await self.collection.delete_one({
            "_id": ObjectId(asset_id),
            "user_id": user_id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        
        return {"message": "Asset deleted successfully"}

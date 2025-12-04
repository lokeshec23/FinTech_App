"""
Asset model and schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum


class AssetType(str, Enum):
    """Asset types"""
    PROPERTY = "Property"
    VEHICLE = "Vehicle"
    INVESTMENT = "Investment"
    JEWELRY = "Jewelry"
    ELECTRONICS = "Electronics"
    OTHERS = "Others"


class AssetBase(BaseModel):
    """Base asset schema"""
    asset_type: AssetType
    name: str = Field(..., min_length=2, max_length=100)
    current_value: float = Field(..., ge=0)
    purchase_value: Optional[float] = Field(None, ge=0)
    purchase_date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=500)


class AssetCreate(AssetBase):
    """Asset creation schema"""
    pass


class AssetUpdate(BaseModel):
    """Asset update schema"""
    asset_type: Optional[AssetType] = None
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    current_value: Optional[float] = Field(None, ge=0)
    purchase_value: Optional[float] = Field(None, ge=0)
    purchase_date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=500)


class AssetResponse(AssetBase):
    """Asset response schema"""
    id: str = Field(..., alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True

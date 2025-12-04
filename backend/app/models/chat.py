"""
Chat model and schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MessageSender(str, Enum):
    """Message sender"""
    USER = "user"
    SUPPORT = "support"
    AI = "ai"


class ChatMessageBase(BaseModel):
    """Base chat message schema"""
    message: str = Field(..., min_length=1, max_length=2000)
    sender: MessageSender


class ChatMessageCreate(BaseModel):
    """Chat message creation schema (user sends)"""
    message: str = Field(..., min_length=1, max_length=2000)


class ChatMessageResponse(ChatMessageBase):
    """Chat message response schema"""
    id: str = Field(..., alias="_id")
    user_id: str
    timestamp: datetime
    read: bool
    created_at: datetime
    
    class Config:
        populate_by_name = True

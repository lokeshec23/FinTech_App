"""
Authentication service
"""
from datetime import datetime, timedelta
from bson import ObjectId
from fastapi import HTTPException, status
from ..models.user import UserCreate, UserInDB, UserLogin, Token, UserResponse
from ..utils.security import hash_password, verify_password, create_access_token
from ..database import get_database


class AuthService:
    """Authentication service"""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.users
    
    async def register_user(self, user_data: UserCreate) -> Token:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.collection.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user document
        user_dict = user_data.dict()
        user_dict["hashed_password"] = hash_password(user_dict.pop("password"))
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        
        # Insert into database
        result = await self.collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        
        # Create access token
        access_token = create_access_token({"sub": str(result.inserted_id)})
        
        # Create user response
        user_response = UserResponse(
            _id=str(result.inserted_id),
            name=user_data.name,
            email=user_data.email,
            phone=user_data.phone,
            created_at=user_dict["created_at"]
        )
        
        return Token(access_token=access_token, user=user_response)
    
    async def login_user(self, login_data: UserLogin) -> Token:
        """Login user"""
        # Find user by email
        user = await self.collection.find_one({"email": login_data.email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(login_data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Create access token
        access_token = create_access_token({"sub": str(user["_id"])})
        
        # Create user response
        user_response = UserResponse(
            _id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            phone=user["phone"],
            created_at=user["created_at"]
        )
        
        return Token(access_token=access_token, user=user_response)
    
    async def get_user_by_id(self, user_id: str) -> UserResponse:
        """Get user by ID"""
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            _id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            phone=user["phone"],
            created_at=user["created_at"]
        )

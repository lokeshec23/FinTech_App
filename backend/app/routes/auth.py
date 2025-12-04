"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException
from ..models.user import UserCreate, UserLogin, Token, UserResponse
from ..services.auth_service import AuthService
from ..utils.security import get_current_user_id

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=201)
async def register(user_data: UserCreate):
    """Register a new user"""
    auth_service = AuthService()
    return await auth_service.register_user(user_data)


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin):
    """Login user"""
    auth_service = AuthService()
    return await auth_service.login_user(login_data)


@router.get("/me", response_model=UserResponse)
async def get_current_user(user_id: str = Depends(get_current_user_id)):
    """Get current authenticated user"""
    auth_service = AuthService()
    return await auth_service.get_user_by_id(user_id)

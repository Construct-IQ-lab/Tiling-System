from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime

from database import get_db
from models.user import User
from services.auth_service import AuthService
from middleware.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str
    company_id: int | None
    is_active: bool
    
    class Config:
        from_attributes = True


@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login endpoint that validates credentials and returns JWT token.
    
    Args:
        form_data: OAuth2 form with username (email) and password
        db: Database session
        
    Returns:
        LoginResponse with access token and user information
    """
    # Find user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not AuthService.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create access token
    access_token = AuthService.create_access_token(data={"sub": str(user.id)})
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.full_name,
            "role": user.role,
            "company_id": user.company_id,
            "is_active": user.is_active
        }
    )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout endpoint (client should discard the token).
    """
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Args:
        current_user: The authenticated user from JWT token
        
    Returns:
        Current user information
    """
    return UserResponse.from_orm(current_user)

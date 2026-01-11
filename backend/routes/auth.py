"""Authentication routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
from backend.database import get_db
from backend.models.user import User
from backend.services.auth_service import verify_password, create_user_token
from backend.middleware.auth import get_current_user

router = APIRouter()


class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response model"""
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    """User info response model"""
    id: str
    email: str
    username: str
    full_name: str | None
    role: str
    company_id: str | None
    company_slug: str | None
    company_name: str | None


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint - authenticate user and return JWT token
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if user is active
    if user.is_active != "true":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Get company info if user has a company
    company_slug = user.company.slug if user.company else None
    company_name = user.company.name if user.company else None
    
    # Create JWT token
    access_token = create_user_token(
        user_id=user.id,
        role=user.role.value,
        company_id=user.company_id,
        company_slug=company_slug
    )
    
    return LoginResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role.value,
            "company_id": user.company_id,
            "company_slug": company_slug,
            "company_name": company_name
        }
    )


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout endpoint - client should discard the token
    """
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    company_slug = current_user.company.slug if current_user.company else None
    company_name = current_user.company.name if current_user.company else None
    
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        role=current_user.role.value,
        company_id=current_user.company_id,
        company_slug=company_slug,
        company_name=company_name
    )

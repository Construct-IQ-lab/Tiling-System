from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from database import get_db
from models.user import User, UserRole
from models.company import Company
from services.auth_service import AuthService

# Security scheme for Bearer token
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer token credentials
        db: Database session
        
    Returns:
        User: The authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = AuthService.verify_token(token)
    
    if payload is None:
        raise credentials_exception
    
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    return user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to require admin role.
    
    Args:
        current_user: The current authenticated user
        
    Returns:
        User: The admin user
        
    Raises:
        HTTPException: If user is not an admin
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def require_company_access(
    company_slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> tuple[User, Company]:
    """
    Dependency to verify user has access to a specific company.
    
    Args:
        company_slug: Company slug from URL path
        current_user: The current authenticated user
        db: Database session
        
    Returns:
        tuple: (User, Company) if access is granted
        
    Raises:
        HTTPException: If company not found or user doesn't have access
    """
    # Admin users have access to all companies
    if current_user.role == UserRole.ADMIN:
        company = db.query(Company).filter(Company.slug == company_slug).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )
        return current_user, company
    
    # Regular users can only access their own company
    if current_user.company is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not associated with any company"
        )
    
    if current_user.company.slug != company_slug:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this company"
        )
    
    return current_user, current_user.company

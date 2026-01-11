from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models.user import User, UserRole
from services.auth_service import verify_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Extract and validate JWT from Bearer token, return current user.
    
    Args:
        credentials: HTTP Authorization credentials with Bearer token
        db: Database session
        
    Returns:
        User: The authenticated user
        
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Ensure the current user has admin role.
    
    Args:
        current_user: The authenticated user
        
    Returns:
        User: The authenticated admin user
        
    Raises:
        HTTPException: 403 if user is not an admin
    """
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_company_access(slug: str):
    """
    Verify user can access specific company data.
    
    Args:
        slug: The company slug to check access for
        
    Returns:
        Callable: Dependency function that validates company access
    """
    async def _check_access(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        # Admin users can access all companies
        if current_user.role == UserRole.admin:
            return current_user
        
        # Company users can only access their own company
        if current_user.company_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not associated with any company"
            )
        
        # Get the company from the slug
        from models.company import Company
        company = db.query(Company).filter(Company.slug == slug).first()
        
        if company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )
        
        if current_user.company_id != company.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this company"
            )
        
        return current_user
    
    return _check_access

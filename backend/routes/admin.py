from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import uuid
import re
from database import get_db
from models.company import Company, CompanyStatus
from models.user import User, UserRole
from models.project import Project
from middleware.auth import require_admin
from services.auth_service import get_password_hash

router = APIRouter()


# Pydantic models
class CompanyCreate(BaseModel):
    name: str
    slug: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    primary_color: Optional[str] = "#1a73e8"
    secondary_color: Optional[str] = "#34a853"
    subscription_plan: Optional[str] = "basic"


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    status: Optional[CompanyStatus] = None
    subscription_plan: Optional[str] = None


class CompanyResponse(BaseModel):
    id: str
    name: str
    slug: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    logo_url: Optional[str]
    primary_color: str
    secondary_color: str
    status: str
    subscription_plan: str
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: UserRole
    company_id: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    company_id: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    company_id: Optional[str]
    company_name: Optional[str]
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime


class DashboardStats(BaseModel):
    total_companies: int
    total_projects: int
    total_users: int


def validate_slug(slug: str) -> bool:
    """Validate slug format: lowercase, alphanumeric, and hyphens only"""
    return bool(re.match(r'^[a-z0-9-]+$', slug))


# Company Management Routes
@router.get("/companies", response_model=List[CompanyResponse])
async def list_companies(
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
    _: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """List all companies with pagination"""
    offset = (page - 1) * per_page
    companies = db.query(Company).offset(offset).limit(per_page).all()
    
    return [
        CompanyResponse(
            id=c.id,
            name=c.name,
            slug=c.slug,
            email=c.email,
            phone=c.phone,
            address=c.address,
            logo_url=c.logo_url,
            primary_color=c.primary_color,
            secondary_color=c.secondary_color,
            status=c.status.value,
            subscription_plan=c.subscription_plan,
            created_at=c.created_at,
            updated_at=c.updated_at
        )
        for c in companies
    ]


@router.post("/companies", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_data: CompanyCreate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new company"""
    # Validate slug format
    if not validate_slug(company_data.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug must be lowercase alphanumeric with hyphens only"
        )
    
    # Check if slug already exists
    existing = db.query(Company).filter(Company.slug == company_data.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company with this slug already exists"
        )
    
    # Create company
    company = Company(
        id=str(uuid.uuid4()),
        name=company_data.name,
        slug=company_data.slug,
        email=company_data.email,
        phone=company_data.phone,
        address=company_data.address,
        primary_color=company_data.primary_color,
        secondary_color=company_data.secondary_color,
        subscription_plan=company_data.subscription_plan,
        status=CompanyStatus.active
    )
    
    db.add(company)
    db.commit()
    db.refresh(company)
    
    return CompanyResponse(
        id=company.id,
        name=company.name,
        slug=company.slug,
        email=company.email,
        phone=company.phone,
        address=company.address,
        logo_url=company.logo_url,
        primary_color=company.primary_color,
        secondary_color=company.secondary_color,
        status=company.status.value,
        subscription_plan=company.subscription_plan,
        created_at=company.created_at,
        updated_at=company.updated_at
    )


@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: str,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get company details by ID"""
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return CompanyResponse(
        id=company.id,
        name=company.name,
        slug=company.slug,
        email=company.email,
        phone=company.phone,
        address=company.address,
        logo_url=company.logo_url,
        primary_color=company.primary_color,
        secondary_color=company.secondary_color,
        status=company.status.value,
        subscription_plan=company.subscription_plan,
        created_at=company.created_at,
        updated_at=company.updated_at
    )


@router.put("/companies/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: str,
    company_data: CompanyUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update company details"""
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Update fields if provided
    update_data = company_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    
    company.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(company)
    
    return CompanyResponse(
        id=company.id,
        name=company.name,
        slug=company.slug,
        email=company.email,
        phone=company.phone,
        address=company.address,
        logo_url=company.logo_url,
        primary_color=company.primary_color,
        secondary_color=company.secondary_color,
        status=company.status.value,
        subscription_plan=company.subscription_plan,
        created_at=company.created_at,
        updated_at=company.updated_at
    )


@router.delete("/companies/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: str,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Soft delete company by setting status to archived"""
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    company.status = CompanyStatus.archived
    company.updated_at = datetime.utcnow()
    db.commit()
    
    return None


# User Management Routes
@router.get("/users", response_model=List[UserResponse])
async def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
    _: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """List all users across companies"""
    offset = (page - 1) * per_page
    users = db.query(User).offset(offset).limit(per_page).all()
    
    return [
        UserResponse(
            id=u.id,
            email=u.email,
            first_name=u.first_name,
            last_name=u.last_name,
            role=u.role.value,
            company_id=u.company_id,
            company_name=u.company.name if u.company else None,
            is_active=u.is_active,
            last_login=u.last_login,
            created_at=u.created_at
        )
        for u in users
    ]


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new user with hashed password"""
    # Check if email already exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Validate company_id if provided
    if user_data.company_id:
        company = db.query(Company).filter(Company.id == user_data.company_id).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company not found"
            )
    
    # Create user with hashed password
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        company_id=user_data.company_id,
        is_active=True
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role.value,
        company_id=user.company_id,
        company_name=user.company.name if user.company else None,
        is_active=user.is_active,
        last_login=user.last_login,
        created_at=user.created_at
    )


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update user details"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields if provided
    update_data = user_data.dict(exclude_unset=True)
    
    # Hash password if being updated
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role.value,
        company_id=user.company_id,
        company_name=user.company.name if user.company else None,
        is_active=user.is_active,
        last_login=user.last_login,
        created_at=user.created_at
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Deactivate user"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    user.updated_at = datetime.utcnow()
    db.commit()
    
    return None


# Dashboard Stats
@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    _: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard statistics"""
    total_companies = db.query(func.count(Company.id)).scalar()
    total_projects = db.query(func.count(Project.id)).scalar()
    total_users = db.query(func.count(User.id)).scalar()
    
    return DashboardStats(
        total_companies=total_companies or 0,
        total_projects=total_projects or 0,
        total_users=total_users or 0
    )

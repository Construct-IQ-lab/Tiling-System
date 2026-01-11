"""Admin routes for managing companies and users"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid
import re
from backend.database import get_db
from backend.models.company import Company, CompanyStatus
from backend.models.user import User, UserRole
from backend.models.project import Project
from backend.middleware.auth import require_admin
from backend.services.auth_service import hash_password

router = APIRouter()


# Pydantic models
class CompanyCreate(BaseModel):
    """Company creation model"""
    name: str
    slug: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: str = "#1976d2"
    secondary_color: str = "#424242"
    subscription_plan: str = "basic"


class CompanyUpdate(BaseModel):
    """Company update model"""
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
    """Company response model"""
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
    user_count: Optional[int] = 0
    project_count: Optional[int] = 0


class UserCreate(BaseModel):
    """User creation model"""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    company_id: Optional[str] = None
    role: UserRole


class UserResponse(BaseModel):
    """User response model"""
    id: str
    email: str
    username: str
    full_name: Optional[str]
    phone: Optional[str]
    company_id: Optional[str]
    company_name: Optional[str]
    role: str
    is_active: str
    created_at: datetime
    last_login: Optional[datetime]


class DashboardStats(BaseModel):
    """Dashboard statistics model"""
    total_companies: int
    active_companies: int
    total_users: int
    total_projects: int


# Helper functions
def validate_slug(slug: str) -> bool:
    """Validate company slug format"""
    return bool(re.match(r'^[a-z0-9-]+$', slug))


# Company routes
@router.get("/companies", response_model=List[CompanyResponse])
def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[CompanyStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """List all companies with optional filtering"""
    query = db.query(Company)
    
    if status:
        query = query.filter(Company.status == status)
    
    companies = query.offset(skip).limit(limit).all()
    
    # Add counts for each company
    result = []
    for company in companies:
        user_count = db.query(User).filter(User.company_id == company.id).count()
        project_count = db.query(Project).filter(Project.company_id == company.id).count()
        
        result.append(CompanyResponse(
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
            updated_at=company.updated_at,
            user_count=user_count,
            project_count=project_count
        ))
    
    return result


@router.post("/companies", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
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
            detail="Company slug already exists"
        )
    
    # Create company
    company = Company(
        id=str(uuid.uuid4()),
        name=company_data.name,
        slug=company_data.slug,
        email=company_data.email,
        phone=company_data.phone,
        address=company_data.address,
        logo_url=company_data.logo_url,
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
        updated_at=company.updated_at,
        user_count=0,
        project_count=0
    )


@router.get("/companies/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get a specific company by ID"""
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    user_count = db.query(User).filter(User.company_id == company.id).count()
    project_count = db.query(Project).filter(Project.company_id == company.id).count()
    
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
        updated_at=company.updated_at,
        user_count=user_count,
        project_count=project_count
    )


@router.put("/companies/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: str,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update a company"""
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Update fields if provided
    update_data = company_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    
    company.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(company)
    
    user_count = db.query(User).filter(User.company_id == company.id).count()
    project_count = db.query(Project).filter(Project.company_id == company.id).count()
    
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
        updated_at=company.updated_at,
        user_count=user_count,
        project_count=project_count
    )


@router.delete("/companies/{company_id}")
def delete_company(
    company_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Archive a company (soft delete)"""
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Archive instead of delete
    company.status = CompanyStatus.archived
    company.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Company archived successfully"}


# User routes
@router.get("/users", response_model=List[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    company_id: Optional[str] = None,
    role: Optional[UserRole] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """List all users with optional filtering"""
    query = db.query(User)
    
    if company_id:
        query = query.filter(User.company_id == company_id)
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.offset(skip).limit(limit).all()
    
    result = []
    for user in users:
        company_name = user.company.name if user.company else None
        result.append(UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            phone=user.phone,
            company_id=user.company_id,
            company_name=company_name,
            role=user.role.value,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login=user.last_login
        ))
    
    return result


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create a new user"""
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # If company_id is provided, verify it exists
    if user_data.company_id:
        company = db.query(Company).filter(Company.id == user_data.company_id).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company not found"
            )
    
    # Create user
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name,
        phone=user_data.phone,
        company_id=user_data.company_id,
        role=user_data.role,
        is_active="true"
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    company_name = user.company.name if user.company else None
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        phone=user.phone,
        company_id=user.company_id,
        company_name=company_name,
        role=user.role.value,
        is_active=user.is_active,
        created_at=user.created_at,
        last_login=user.last_login
    )


# Dashboard statistics
@router.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get dashboard statistics for admin"""
    total_companies = db.query(Company).count()
    active_companies = db.query(Company).filter(Company.status == CompanyStatus.active).count()
    total_users = db.query(User).count()
    total_projects = db.query(Project).count()
    
    return DashboardStats(
        total_companies=total_companies,
        active_companies=active_companies,
        total_users=total_users,
        total_projects=total_projects
    )

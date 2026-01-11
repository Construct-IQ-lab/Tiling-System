from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from database import get_db
from models.company import Company, CompanyStatus, SubscriptionPlan
from models.user import User, UserRole
from models.project import Project, ProjectStatus
from services.auth_service import AuthService
from middleware.auth import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(require_admin)])


# Pydantic models for request/response
class CompanyCreate(BaseModel):
    name: str
    slug: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    primary_color: str = "#3B82F6"
    secondary_color: str = "#10B981"
    subscription_plan: SubscriptionPlan = SubscriptionPlan.FREE


class CompanyResponse(BaseModel):
    id: int
    name: str
    slug: str
    email: str
    phone: Optional[str]
    status: CompanyStatus
    subscription_plan: SubscriptionPlan
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: UserRole
    company_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: UserRole
    company_id: Optional[int]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.get("/companies", response_model=List[CompanyResponse])
async def list_companies(db: Session = Depends(get_db)):
    """
    List all companies in the system.
    """
    companies = db.query(Company).all()
    return companies


@router.post("/companies", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new company.
    """
    # Check if company with same slug or name exists
    existing = db.query(Company).filter(
        (Company.slug == company_data.slug) | (Company.name == company_data.name)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company with this name or slug already exists"
        )
    
    company = Company(**company_data.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    
    return company


@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    """
    Get a specific company by ID.
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return company


@router.put("/companies/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company_data: CompanyCreate,
    db: Session = Depends(get_db)
):
    """
    Update a company.
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    for key, value in company_data.model_dump().items():
        setattr(company, key, value)
    
    company.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(company)
    
    return company


@router.delete("/companies/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, db: Session = Depends(get_db)):
    """
    Delete a company and all associated data.
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    db.delete(company)
    db.commit()
    
    return None


@router.get("/users", response_model=List[UserResponse])
async def list_users(db: Session = Depends(get_db)):
    """
    List all users in the system.
    """
    users = db.query(User).all()
    return users


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user.
    """
    # Check if user with same email exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Hash password
    password_hash = AuthService.get_password_hash(user_data.password)
    
    user = User(
        email=user_data.email,
        password_hash=password_hash,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        company_id=user_data.company_id
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/dashboard")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get admin dashboard statistics.
    """
    total_companies = db.query(func.count(Company.id)).scalar()
    active_companies = db.query(func.count(Company.id)).filter(
        Company.status == CompanyStatus.ACTIVE
    ).scalar()
    
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    
    total_projects = db.query(func.count(Project.id)).scalar()
    active_projects = db.query(func.count(Project.id)).filter(
        Project.status.in_([ProjectStatus.APPROVED, ProjectStatus.IN_PROGRESS])
    ).scalar()
    
    return {
        "companies": {
            "total": total_companies,
            "active": active_companies
        },
        "users": {
            "total": total_users,
            "active": active_users
        },
        "projects": {
            "total": total_projects,
            "active": active_projects
        }
    }

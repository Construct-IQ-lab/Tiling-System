"""Company-specific routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from backend.database import get_db
from backend.models.company import Company
from backend.models.user import User
from backend.models.project import Project
from backend.middleware.auth import get_current_user

router = APIRouter()


# Pydantic models
class CompanyTheme(BaseModel):
    """Company theme/branding model"""
    name: str
    slug: str
    logo_url: Optional[str]
    primary_color: str
    secondary_color: str


class CompanyDashboard(BaseModel):
    """Company dashboard statistics"""
    company_name: str
    total_projects: int
    active_projects: int
    completed_projects: int
    total_users: int


class ProjectSummary(BaseModel):
    """Project summary model"""
    id: str
    name: str
    description: Optional[str]
    client_name: Optional[str]
    status: str
    budget: Optional[float]
    created_at: datetime
    updated_at: datetime


# Helper function to verify company access
def verify_company_access(slug: str, current_user: User, db: Session) -> Company:
    """Verify user has access to company and return company"""
    company = db.query(Company).filter(Company.slug == slug).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Admin can access any company
    from backend.models.user import UserRole
    if current_user.role == UserRole.admin:
        return company
    
    # Company users can only access their own company
    if not current_user.company_id or current_user.company_id != company.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this company"
        )
    
    return company


@router.get("/{slug}/theme", response_model=CompanyTheme)
def get_company_theme(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get company theme/branding information"""
    company = verify_company_access(slug, current_user, db)
    
    return CompanyTheme(
        name=company.name,
        slug=company.slug,
        logo_url=company.logo_url,
        primary_color=company.primary_color,
        secondary_color=company.secondary_color
    )


@router.get("/{slug}/dashboard", response_model=CompanyDashboard)
def get_company_dashboard(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get company dashboard statistics"""
    company = verify_company_access(slug, current_user, db)
    
    total_projects = db.query(Project).filter(Project.company_id == company.id).count()
    active_projects = db.query(Project).filter(
        Project.company_id == company.id,
        Project.status.in_(["planning", "in_progress"])
    ).count()
    completed_projects = db.query(Project).filter(
        Project.company_id == company.id,
        Project.status == "completed"
    ).count()
    total_users = db.query(User).filter(User.company_id == company.id).count()
    
    return CompanyDashboard(
        company_name=company.name,
        total_projects=total_projects,
        active_projects=active_projects,
        completed_projects=completed_projects,
        total_users=total_users
    )


@router.get("/{slug}/projects", response_model=List[ProjectSummary])
def get_company_projects(
    slug: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get company's projects"""
    company = verify_company_access(slug, current_user, db)
    
    query = db.query(Project).filter(Project.company_id == company.id)
    
    if status:
        query = query.filter(Project.status == status)
    
    projects = query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        ProjectSummary(
            id=p.id,
            name=p.name,
            description=p.description,
            client_name=p.client_name,
            status=p.status,
            budget=float(p.budget) if p.budget else None,
            created_at=p.created_at,
            updated_at=p.updated_at
        )
        for p in projects
    ]

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
import uuid
from database import get_db
from models.company import Company
from models.project import Project, ProjectStatus
from models.quote import Quote, QuoteStatus
from models.user import User, UserRole
from middleware.auth import get_current_user

router = APIRouter()


def check_company_access(slug: str, current_user: User, db: Session) -> Company:
    """
    Helper function to verify user can access specific company data.
    Returns the company if access is granted, raises HTTPException otherwise.
    """
    company = db.query(Company).filter(Company.slug == slug).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Admin users can access all companies
    if current_user.role == UserRole.admin:
        return company
    
    # Company users can only access their own company
    if current_user.company_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not associated with any company"
        )
    
    if current_user.company_id != company.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this company"
        )
    
    return company


# Pydantic models
class CompanyTheme(BaseModel):
    logo_url: Optional[str]
    primary_color: str
    secondary_color: str
    company_name: str


class CompanyDashboardStats(BaseModel):
    total_projects: int
    active_projects: int
    completed_projects: int


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    client_name: Optional[str] = None
    client_email: Optional[EmailStr] = None
    client_phone: Optional[str] = None
    measurements: Optional[dict] = None
    tiles: Optional[dict] = None
    materials: Optional[dict] = None
    budget: Optional[float] = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    company_id: str
    created_by: str
    client_name: Optional[str]
    client_email: Optional[str]
    client_phone: Optional[str]
    measurements: Optional[dict]
    tiles: Optional[dict]
    materials: Optional[dict]
    status: str
    budget: Optional[float]
    created_at: datetime
    updated_at: datetime


class QuoteCreate(BaseModel):
    client_name: str
    client_email: EmailStr
    client_phone: Optional[str] = None
    project_id: Optional[str] = None
    total_amount: float
    valid_until: datetime


class QuoteResponse(BaseModel):
    id: str
    quote_number: str
    company_id: str
    project_id: Optional[str]
    client_name: str
    client_email: str
    client_phone: Optional[str]
    total_amount: float
    status: str
    valid_until: datetime
    created_at: datetime
    updated_at: datetime


@router.get("/{slug}/theme", response_model=CompanyTheme)
async def get_company_theme(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Public endpoint returning company theme (logo, colors).
    Used for dynamic branding of the company portal.
    """
    company = db.query(Company).filter(Company.slug == slug).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return CompanyTheme(
        logo_url=company.logo_url,
        primary_color=company.primary_color,
        secondary_color=company.secondary_color,
        company_name=company.name
    )


@router.get("/{slug}/dashboard", response_model=CompanyDashboardStats)
async def get_company_dashboard(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics for a specific company"""
    company = check_company_access(slug, current_user, db)
    
    # Count projects by status
    total_projects = db.query(func.count(Project.id)).filter(
        Project.company_id == company.id
    ).scalar()
    
    active_projects = db.query(func.count(Project.id)).filter(
        Project.company_id == company.id,
        Project.status == ProjectStatus.in_progress
    ).scalar()
    
    completed_projects = db.query(func.count(Project.id)).filter(
        Project.company_id == company.id,
        Project.status == ProjectStatus.completed
    ).scalar()
    
    return CompanyDashboardStats(
        total_projects=total_projects or 0,
        active_projects=active_projects or 0,
        completed_projects=completed_projects or 0
    )


@router.get("/{slug}/projects", response_model=List[ProjectResponse])
async def list_company_projects(
    slug: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all projects for a specific company with pagination"""
    company = check_company_access(slug, current_user, db)
    
    offset = (page - 1) * per_page
    projects = db.query(Project).filter(
        Project.company_id == company.id
    ).offset(offset).limit(per_page).all()
    
    return [
        ProjectResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            company_id=p.company_id,
            created_by=p.created_by,
            client_name=p.client_name,
            client_email=p.client_email,
            client_phone=p.client_phone,
            measurements=p.measurements,
            tiles=p.tiles,
            materials=p.materials,
            status=p.status.value,
            budget=p.budget,
            created_at=p.created_at,
            updated_at=p.updated_at
        )
        for p in projects
    ]


@router.post("/{slug}/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_company_project(
    slug: str,
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new project for a specific company"""
    company = check_company_access(slug, current_user, db)
    
    # Create project
    project = Project(
        id=str(uuid.uuid4()),
        name=project_data.name,
        description=project_data.description,
        company_id=company.id,
        created_by=current_user.id,
        client_name=project_data.client_name,
        client_email=project_data.client_email,
        client_phone=project_data.client_phone,
        measurements=project_data.measurements,
        tiles=project_data.tiles,
        materials=project_data.materials,
        budget=project_data.budget,
        status=ProjectStatus.planning
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        company_id=project.company_id,
        created_by=project.created_by,
        client_name=project.client_name,
        client_email=project.client_email,
        client_phone=project.client_phone,
        measurements=project.measurements,
        tiles=project.tiles,
        materials=project.materials,
        status=project.status.value,
        budget=project.budget,
        created_at=project.created_at,
        updated_at=project.updated_at
    )


@router.get("/{slug}/quotes", response_model=List[QuoteResponse])
async def list_company_quotes(
    slug: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all quotes for a specific company with pagination"""
    company = check_company_access(slug, current_user, db)
    
    offset = (page - 1) * per_page
    quotes = db.query(Quote).filter(
        Quote.company_id == company.id
    ).offset(offset).limit(per_page).all()
    
    return [
        QuoteResponse(
            id=q.id,
            quote_number=q.quote_number,
            company_id=q.company_id,
            project_id=q.project_id,
            client_name=q.client_name,
            client_email=q.client_email,
            client_phone=q.client_phone,
            total_amount=q.total_amount,
            status=q.status.value,
            valid_until=q.valid_until,
            created_at=q.created_at,
            updated_at=q.updated_at
        )
        for q in quotes
    ]


@router.post("/{slug}/quotes", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_company_quote(
    slug: str,
    quote_data: QuoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new quote for a specific company"""
    company = check_company_access(slug, current_user, db)
    
    # Generate quote number (simple format: QT-{timestamp}-{random})
    quote_number = f"QT-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    # Validate project_id if provided
    if quote_data.project_id:
        project = db.query(Project).filter(
            Project.id == quote_data.project_id,
            Project.company_id == company.id
        ).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project not found or does not belong to this company"
            )
    
    # Create quote
    quote = Quote(
        id=str(uuid.uuid4()),
        quote_number=quote_number,
        company_id=company.id,
        project_id=quote_data.project_id,
        client_name=quote_data.client_name,
        client_email=quote_data.client_email,
        client_phone=quote_data.client_phone,
        total_amount=quote_data.total_amount,
        valid_until=quote_data.valid_until,
        status=QuoteStatus.draft
    )
    
    db.add(quote)
    db.commit()
    db.refresh(quote)
    
    return QuoteResponse(
        id=quote.id,
        quote_number=quote.quote_number,
        company_id=quote.company_id,
        project_id=quote.project_id,
        client_name=quote.client_name,
        client_email=quote.client_email,
        client_phone=quote.client_phone,
        total_amount=quote.total_amount,
        status=quote.status.value,
        valid_until=quote.valid_until,
        created_at=quote.created_at,
        updated_at=quote.updated_at
    )

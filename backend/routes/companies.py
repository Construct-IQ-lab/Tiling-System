from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List
from datetime import datetime

from database import get_db
from models.company import Company
from models.user import User
from models.project import Project, ProjectStatus
from models.quote import Quote, QuoteStatus
from models.invoice import Invoice, InvoiceStatus
from middleware.auth import require_company_access

router = APIRouter(prefix="/companies", tags=["Companies"])


class ProjectResponse(BaseModel):
    id: int
    name: str
    client_name: str
    status: ProjectStatus
    budget: float | None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ThemeResponse(BaseModel):
    primary_color: str
    secondary_color: str
    logo_url: str | None
    company_name: str


@router.get("/{company_slug}/dashboard")
async def get_company_dashboard(
    company_slug: str,
    user_company: tuple[User, Company] = Depends(require_company_access),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics for a specific company.
    """
    current_user, company = user_company
    
    # Project statistics
    total_projects = db.query(func.count(Project.id)).filter(
        Project.company_id == company.id
    ).scalar()
    
    active_projects = db.query(func.count(Project.id)).filter(
        Project.company_id == company.id,
        Project.status.in_([ProjectStatus.APPROVED, ProjectStatus.IN_PROGRESS])
    ).scalar()
    
    completed_projects = db.query(func.count(Project.id)).filter(
        Project.company_id == company.id,
        Project.status == ProjectStatus.COMPLETED
    ).scalar()
    
    # Quote statistics
    total_quotes = db.query(func.count(Quote.id)).filter(
        Quote.company_id == company.id
    ).scalar()
    
    pending_quotes = db.query(func.count(Quote.id)).filter(
        Quote.company_id == company.id,
        Quote.status == QuoteStatus.SENT
    ).scalar()
    
    # Invoice statistics
    total_invoices = db.query(func.count(Invoice.id)).filter(
        Invoice.company_id == company.id
    ).scalar()
    
    outstanding_invoices = db.query(func.count(Invoice.id)).filter(
        Invoice.company_id == company.id,
        Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.OVERDUE])
    ).scalar()
    
    # Revenue calculation
    total_revenue = db.query(func.sum(Invoice.total_amount)).filter(
        Invoice.company_id == company.id,
        Invoice.status == InvoiceStatus.PAID
    ).scalar() or 0
    
    return {
        "company": {
            "id": company.id,
            "name": company.name,
            "slug": company.slug,
            "subscription_plan": company.subscription_plan
        },
        "projects": {
            "total": total_projects,
            "active": active_projects,
            "completed": completed_projects
        },
        "quotes": {
            "total": total_quotes,
            "pending": pending_quotes
        },
        "invoices": {
            "total": total_invoices,
            "outstanding": outstanding_invoices
        },
        "revenue": {
            "total": float(total_revenue)
        }
    }


@router.get("/{company_slug}/projects", response_model=List[ProjectResponse])
async def list_company_projects(
    company_slug: str,
    user_company: tuple[User, Company] = Depends(require_company_access),
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """
    List all projects for a specific company.
    """
    current_user, company = user_company
    
    projects = db.query(Project).filter(
        Project.company_id == company.id
    ).order_by(
        Project.created_at.desc()
    ).limit(limit).offset(offset).all()
    
    return projects


@router.get("/{company_slug}/theme", response_model=ThemeResponse)
async def get_company_theme(
    company_slug: str,
    user_company: tuple[User, Company] = Depends(require_company_access)
):
    """
    Get company branding/theme information.
    """
    current_user, company = user_company
    
    return ThemeResponse(
        primary_color=company.primary_color,
        secondary_color=company.secondary_color,
        logo_url=company.logo_url,
        company_name=company.name
    )

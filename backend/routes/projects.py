from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from database import get_db
from models.project import Project, ProjectStatus
from models.company import Company
from models.user import User, UserRole
from middleware.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


# Helper function for access control
def verify_project_access(project: Project, current_user: User) -> None:
    """
    Verify that the current user has access to the project.
    Raises HTTPException if access is denied.
    
    Args:
        project: The project to check access for
        current_user: The current authenticated user
        
    Raises:
        HTTPException: If user doesn't have access to the project
    """
    # Admin users have access to all projects
    if current_user.role == UserRole.ADMIN:
        return
    
    # Regular users can only access projects in their company
    if current_user.company_id != project.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this project"
        )


# Pydantic models for request/response
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    client_name: str = Field(..., min_length=1, max_length=255)
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    room_length: Optional[float] = Field(None, gt=0)
    room_width: Optional[float] = Field(None, gt=0)
    tile_length: Optional[float] = Field(None, gt=0)
    tile_width: Optional[float] = Field(None, gt=0)
    tile_price_per_unit: Optional[float] = Field(None, ge=0)
    wastage_percentage: float = Field(10.0, ge=0, le=100)
    budget: Optional[float] = Field(None, ge=0)
    company_id: Optional[int] = Field(None, description="Company ID (required for admin users)")


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    client_name: Optional[str] = Field(None, min_length=1, max_length=255)
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    client_address: Optional[str] = None
    room_length: Optional[float] = Field(None, gt=0)
    room_width: Optional[float] = Field(None, gt=0)
    tile_length: Optional[float] = Field(None, gt=0)
    tile_width: Optional[float] = Field(None, gt=0)
    tile_price_per_unit: Optional[float] = Field(None, ge=0)
    wastage_percentage: Optional[float] = Field(None, ge=0, le=100)
    status: Optional[ProjectStatus] = None
    budget: Optional[float] = Field(None, ge=0)
    actual_cost: Optional[float] = Field(None, ge=0)


class ProjectResponse(BaseModel):
    id: int
    company_id: int
    created_by: Optional[int]
    name: str
    description: Optional[str]
    client_name: str
    client_email: Optional[str]
    client_phone: Optional[str]
    client_address: Optional[str]
    room_length: Optional[float]
    room_width: Optional[float]
    room_area: Optional[float]
    tile_length: Optional[float]
    tile_width: Optional[float]
    tile_price_per_unit: Optional[float]
    wastage_percentage: Optional[float]
    status: ProjectStatus
    budget: Optional[float]
    actual_cost: Optional[float]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    status: Optional[ProjectStatus] = None
):
    """
    List all projects accessible to the current user.
    Admins see all projects, company users only see their company's projects.
    """
    query = db.query(Project)
    
    # Filter by company for non-admin users
    if current_user.role != UserRole.ADMIN:
        if current_user.company_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not associated with any company"
            )
        query = query.filter(Project.company_id == current_user.company_id)
    
    # Optional status filter
    if status:
        query = query.filter(Project.status == status)
    
    projects = query.order_by(
        Project.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return projects


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new project.
    Company users can only create projects for their own company.
    Admin users must specify a company_id in the request.
    """
    # Determine company_id
    if current_user.role == UserRole.ADMIN:
        # Admin users must provide company_id
        if not project_data.company_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin users must specify a company_id when creating projects"
            )
        company_id = project_data.company_id
        
        # Verify the company exists
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )
    else:
        # Non-admin users use their own company
        if current_user.company_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not associated with any company"
            )
        company_id = current_user.company_id
    
    # Calculate room area if dimensions provided
    room_area = None
    if project_data.room_length and project_data.room_width:
        room_area = project_data.room_length * project_data.room_width
    
    project = Project(
        company_id=company_id,
        created_by=current_user.id,
        name=project_data.name,
        description=project_data.description,
        client_name=project_data.client_name,
        client_email=project_data.client_email,
        client_phone=project_data.client_phone,
        client_address=project_data.client_address,
        room_length=project_data.room_length,
        room_width=project_data.room_width,
        room_area=room_area,
        tile_length=project_data.tile_length,
        tile_width=project_data.tile_width,
        tile_price_per_unit=project_data.tile_price_per_unit,
        wastage_percentage=project_data.wastage_percentage,
        budget=project_data.budget
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific project by ID.
    Users can only access projects in their company (unless admin).
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check access rights using helper function
    verify_project_access(project, current_user)
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a project.
    Users can only update projects in their company (unless admin).
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check access rights using helper function
    verify_project_access(project, current_user)
    
    # Update fields
    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    # Recalculate room area if dimensions changed
    if "room_length" in update_data or "room_width" in update_data:
        if project.room_length and project.room_width:
            project.room_area = project.room_length * project.room_width
    
    # Update completed_at timestamp if status changed to completed
    if project_data.status == ProjectStatus.COMPLETED and project.status != ProjectStatus.COMPLETED:
        project.completed_at = datetime.utcnow()
    
    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a project.
    Users can only delete projects in their company (unless admin).
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check access rights using helper function
    verify_project_access(project, current_user)
    
    db.delete(project)
    db.commit()
    
    return None

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
from database import get_db
from models.project import Project, ProjectStatus
from models.user import User
from middleware.auth import get_current_user

router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    client_name: Optional[str] = None
    measurements: Optional[dict] = None
    tiles: Optional[dict] = None
    materials: Optional[dict] = None
    budget: Optional[float] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
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
    status: str
    budget: Optional[float]
    created_at: datetime
    updated_at: datetime


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List projects accessible to the current user"""
    # Admin can see all projects
    if current_user.role.value == "admin":
        projects = db.query(Project).all()
    else:
        # Company users see only their company's projects
        if not current_user.company_id:
            return []
        projects = db.query(Project).filter(Project.company_id == current_user.company_id).all()
    
    return [
        ProjectResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            company_id=p.company_id,
            created_by=p.created_by,
            status=p.status.value,
            budget=p.budget,
            created_at=p.created_at,
            updated_at=p.updated_at
        )
        for p in projects
    ]


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get project by ID"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check access
    if current_user.role.value != "admin" and project.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this project"
        )
    
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        company_id=project.company_id,
        created_by=project.created_by,
        status=project.status.value,
        budget=project.budget,
        created_at=project.created_at,
        updated_at=project.updated_at
    )


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new project"""
    if not current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must be associated with a company to create projects"
        )
    
    project = Project(
        id=str(uuid.uuid4()),
        name=project_data.name,
        description=project_data.description,
        company_id=current_user.company_id,
        created_by=current_user.id,
        client_name=project_data.client_name,
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
        status=project.status.value,
        budget=project.budget,
        created_at=project.created_at,
        updated_at=project.updated_at
    )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check access
    if current_user.role.value != "admin" and project.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this project"
        )
    
    # Update fields
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        company_id=project.company_id,
        created_by=project.created_by,
        status=project.status.value,
        budget=project.budget,
        created_at=project.created_at,
        updated_at=project.updated_at
    )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check access
    if current_user.role.value != "admin" and project.company_id != current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this project"
        )
    
    db.delete(project)
    db.commit()
    
    return None

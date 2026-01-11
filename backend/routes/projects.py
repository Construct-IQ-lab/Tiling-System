from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from database import get_db
from models.project import Project, ProjectStatus


# Pydantic Schemas
class ProjectCreate(BaseModel):
    """Schema for creating a project"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    client_name: Optional[str] = None
    client_contact: Optional[str] = None
    client_address: Optional[str] = None
    length: Optional[float] = None
    width: Optional[float] = None
    area: Optional[float] = None
    measurement_unit: str = "meters"
    tile_type: Optional[str] = None
    tile_size: Optional[str] = None
    tile_quantity: Optional[int] = None
    wastage_percent: float = 10.0
    status: Optional[ProjectStatus] = ProjectStatus.PLANNING
    budget: Optional[float] = None
    actual_cost: Optional[float] = None


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    client_name: Optional[str] = None
    client_contact: Optional[str] = None
    client_address: Optional[str] = None
    length: Optional[float] = None
    width: Optional[float] = None
    area: Optional[float] = None
    measurement_unit: Optional[str] = None
    tile_type: Optional[str] = None
    tile_size: Optional[str] = None
    tile_quantity: Optional[int] = None
    wastage_percent: Optional[float] = None
    status: Optional[ProjectStatus] = None
    budget: Optional[float] = None
    actual_cost: Optional[float] = None


class ProjectResponse(BaseModel):
    """Schema for project response"""
    id: int
    name: str
    description: Optional[str]
    client_name: Optional[str]
    client_contact: Optional[str]
    client_address: Optional[str]
    length: Optional[float]
    width: Optional[float]
    area: Optional[float]
    measurement_unit: str
    tile_type: Optional[str]
    tile_size: Optional[str]
    tile_quantity: Optional[int]
    wastage_percent: float
    status: ProjectStatus
    budget: Optional[float]
    actual_cost: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Router
router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get("/", response_model=List[ProjectResponse])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all projects with pagination"""
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get a project by ID"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    """Update a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update only provided fields
    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return None

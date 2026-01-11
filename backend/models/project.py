from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class ProjectStatus(str, enum.Enum):
    planning = "planning"
    in_progress = "in_progress"
    completed = "completed"
    on_hold = "on_hold"
    cancelled = "cancelled"


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    
    # Multi-tenant fields
    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Client information
    client_name = Column(String)
    client_email = Column(String)
    client_phone = Column(String)
    
    # Measurements and calculations
    measurements = Column(JSON)  # Store area, dimensions, etc.
    tiles = Column(JSON)  # Tile specifications
    materials = Column(JSON)  # Material list and quantities
    
    # Project details
    status = Column(Enum(ProjectStatus), default=ProjectStatus.planning, nullable=False)
    budget = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="projects")
    creator = relationship("User", back_populates="created_projects")
    quotes = relationship("Quote", back_populates="project")
    invoices = relationship("Invoice", back_populates="project")

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum


class ProjectStatus(str, enum.Enum):
    """Project status enumeration"""
    PLANNING = "planning"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(Base):
    """Project model for tiling projects"""
    __tablename__ = "projects"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Project Information
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    # Client Information
    client_name = Column(String, nullable=True)
    client_contact = Column(String, nullable=True)
    client_address = Column(String, nullable=True)
    
    # Measurements
    length = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    area = Column(Float, nullable=True)
    measurement_unit = Column(String, default="meters")
    
    # Tile Information
    tile_type = Column(String, nullable=True)
    tile_size = Column(String, nullable=True)
    tile_quantity = Column(Integer, nullable=True)
    wastage_percent = Column(Float, default=10.0)
    
    # Status and Budget
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING)
    budget = Column(Float, nullable=True)
    actual_cost = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class ProjectStatus(str, enum.Enum):
    INQUIRY = "inquiry"
    QUOTED = "quoted"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Project details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Client details
    client_name = Column(String(255), nullable=False)
    client_email = Column(String(255))
    client_phone = Column(String(50))
    client_address = Column(String(500))
    
    # Measurements
    room_length = Column(Numeric(10, 2))  # in meters or feet
    room_width = Column(Numeric(10, 2))
    room_area = Column(Numeric(10, 2))
    
    # Tile information
    tile_length = Column(Numeric(10, 2))
    tile_width = Column(Numeric(10, 2))
    tile_price_per_unit = Column(Numeric(10, 2))
    wastage_percentage = Column(Numeric(5, 2), default=10.0)
    
    # Project status and financials
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.INQUIRY)
    budget = Column(Numeric(12, 2))
    actual_cost = Column(Numeric(12, 2))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationships
    company = relationship("Company", back_populates="projects")
    creator = relationship("User", back_populates="created_projects", foreign_keys=[created_by])
    quotes = relationship("Quote", back_populates="project", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"

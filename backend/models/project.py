from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class Project(Base):
    """Project model with company association"""
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Multi-tenant fields
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # Client information
    client_name = Column(String(255))
    client_email = Column(String(255))
    client_phone = Column(String(50))
    client_address = Column(String(500))
    
    # Project details
    status = Column(String(50), default="planning")  # planning, in_progress, completed, on_hold, cancelled
    
    # Measurements and calculations (stored as JSON)
    measurements = Column(JSON)
    tiles = Column(JSON)
    materials = Column(JSON)
    
    # Budget
    budget = Column(Numeric(10, 2))
    estimated_cost = Column(Numeric(10, 2))
    actual_cost = Column(Numeric(10, 2))
    
    # Timeline
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="projects")
    creator = relationship("User", back_populates="created_projects", foreign_keys=[created_by])
    quotes = relationship("Quote", back_populates="project")
    invoices = relationship("Invoice", back_populates="project")

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, company_id={self.company_id}, status={self.status})>"

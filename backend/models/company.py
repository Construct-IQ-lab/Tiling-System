from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from backend.database import Base


class CompanyStatus(str, enum.Enum):
    """Company status enumeration"""
    active = "active"
    suspended = "suspended"
    archived = "archived"


class Company(Base):
    """Company model for multi-tenant system"""
    __tablename__ = "companies"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    address = Column(String(500))
    
    # Branding
    logo_url = Column(String(500))
    primary_color = Column(String(7), default="#1976d2")  # Hex color
    secondary_color = Column(String(7), default="#424242")  # Hex color
    
    # Status and subscription
    status = Column(Enum(CompanyStatus), default=CompanyStatus.active, nullable=False)
    subscription_plan = Column(String(50), default="basic")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="company")
    projects = relationship("Project", back_populates="company")
    quotes = relationship("Quote", back_populates="company")
    invoices = relationship("Invoice", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name}, slug={self.slug}, status={self.status})>"

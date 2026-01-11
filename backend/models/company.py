from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class CompanyStatus(str, enum.Enum):
    active = "active"
    suspended = "suspended"
    archived = "archived"


class Company(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    
    # Branding
    logo_url = Column(String)
    primary_color = Column(String, default="#1a73e8")
    secondary_color = Column(String, default="#34a853")
    
    # Management
    status = Column(Enum(CompanyStatus), default=CompanyStatus.active, nullable=False)
    subscription_plan = Column(String, default="basic")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="company")
    projects = relationship("Project", back_populates="company")
    quotes = relationship("Quote", back_populates="company")
    invoices = relationship("Invoice", back_populates="company")

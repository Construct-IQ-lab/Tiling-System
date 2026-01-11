from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from backend.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    admin = "admin"
    company_owner = "company_owner"
    company_staff = "company_staff"


class User(Base):
    """User model with multi-tenant support"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # User details
    full_name = Column(String(255))
    phone = Column(String(50))
    
    # Multi-tenant fields
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True, index=True)
    role = Column(Enum(UserRole), default=UserRole.company_staff, nullable=False)
    
    # Status
    is_active = Column(String(10), default="true")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime)
    
    # Relationships
    company = relationship("Company", back_populates="users")
    created_projects = relationship("Project", back_populates="creator", foreign_keys="Project.created_by")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role}, company_id={self.company_id})>"

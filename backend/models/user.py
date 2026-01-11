from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    OWNER = "owner"
    MANAGER = "manager"
    STAFF = "staff"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STAFF)
    phone = Column(String(50))
    avatar_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="users")
    created_projects = relationship("Project", back_populates="creator", foreign_keys="Project.created_by")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"

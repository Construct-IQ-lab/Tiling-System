from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class CompanyStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRIAL = "trial"


class SubscriptionPlan(str, enum.Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    address = Column(String(500))
    logo_url = Column(String(500))
    primary_color = Column(String(7), default="#3B82F6")  # Hex color code
    secondary_color = Column(String(7), default="#10B981")  # Hex color code
    status = Column(SQLEnum(CompanyStatus), default=CompanyStatus.TRIAL)
    subscription_plan = Column(SQLEnum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="company", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="company", cascade="all, delete-orphan")
    quotes = relationship("Quote", back_populates="company", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="company", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', slug='{self.slug}')>"

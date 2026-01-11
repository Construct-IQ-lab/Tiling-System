from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class QuoteStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    approved = "approved"
    rejected = "rejected"


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(String, primary_key=True, index=True)
    quote_number = Column(String, unique=True, nullable=False, index=True)
    
    # Company and project association
    company_id = Column(String, ForeignKey("companies.id"), nullable=False, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    
    # Client details
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    client_phone = Column(String)
    
    # Quote details
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(QuoteStatus), default=QuoteStatus.draft, nullable=False)
    
    # Dates
    valid_until = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="quotes")
    project = relationship("Project", back_populates="quotes")

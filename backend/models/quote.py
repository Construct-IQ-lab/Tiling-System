from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Date, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from backend.database import Base


class QuoteStatus(str, enum.Enum):
    """Quote status enumeration"""
    draft = "draft"
    sent = "sent"
    approved = "approved"
    rejected = "rejected"


class Quote(Base):
    """Quote model for project estimates"""
    __tablename__ = "quotes"

    id = Column(String(36), primary_key=True, index=True)
    quote_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relations
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    
    # Client information
    client_name = Column(String(255), nullable=False)
    client_email = Column(String(255))
    client_phone = Column(String(50))
    client_address = Column(String(500))
    
    # Quote details
    description = Column(String(1000))
    items = Column(JSON)  # List of line items with description, quantity, rate, amount
    
    # Amounts
    subtotal = Column(Numeric(10, 2), nullable=False, default=0)
    tax_rate = Column(Numeric(5, 2), default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0)
    
    # Status and validity
    status = Column(Enum(QuoteStatus), default=QuoteStatus.draft, nullable=False)
    valid_until = Column(Date)
    
    # Notes
    notes = Column(String(2000))
    terms_and_conditions = Column(String(2000))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    sent_at = Column(DateTime)
    approved_at = Column(DateTime)
    
    # Relationships
    company = relationship("Company", back_populates="quotes")
    project = relationship("Project", back_populates="quotes")

    def __repr__(self):
        return f"<Quote(id={self.id}, quote_number={self.quote_number}, status={self.status}, total={self.total_amount})>"

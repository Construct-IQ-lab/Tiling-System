from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import enum
from database import Base


class QuoteStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    
    quote_number = Column(String(50), nullable=False, unique=True, index=True)
    
    # Client details
    client_name = Column(String(255), nullable=False)
    client_email = Column(String(255), nullable=False)
    client_phone = Column(String(50))
    client_address = Column(String(500))
    
    # Financial details
    total_amount = Column(Numeric(12, 2), nullable=False)
    tax_amount = Column(Numeric(12, 2), default=0.0)
    discount_amount = Column(Numeric(12, 2), default=0.0)
    
    # Quote status and validity
    status = Column(SQLEnum(QuoteStatus), default=QuoteStatus.DRAFT)
    valid_until = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))
    
    # Additional information
    notes = Column(Text)
    terms_and_conditions = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime)
    accepted_at = Column(DateTime)

    # Relationships
    company = relationship("Company", back_populates="quotes")
    project = relationship("Project", back_populates="quotes")

    def __repr__(self):
        return f"<Quote(id={self.id}, quote_number='{self.quote_number}', status='{self.status}')>"

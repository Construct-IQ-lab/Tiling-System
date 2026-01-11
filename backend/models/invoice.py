from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Date, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from backend.database import Base


class InvoiceStatus(str, enum.Enum):
    """Invoice status enumeration"""
    pending = "pending"
    paid = "paid"
    overdue = "overdue"
    cancelled = "cancelled"


class Invoice(Base):
    """Invoice model for project billing"""
    __tablename__ = "invoices"

    id = Column(String(36), primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relations
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    
    # Client information
    client_name = Column(String(255), nullable=False)
    client_email = Column(String(255))
    client_phone = Column(String(50))
    client_address = Column(String(500))
    
    # Invoice details
    description = Column(String(1000))
    items = Column(JSON)  # List of line items
    
    # Amounts
    subtotal = Column(Numeric(10, 2), nullable=False, default=0)
    tax_rate = Column(Numeric(5, 2), default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    amount = Column(Numeric(10, 2), nullable=False, default=0)
    amount_paid = Column(Numeric(10, 2), default=0)
    
    # Status and dates
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.pending, nullable=False)
    due_date = Column(Date, nullable=False)
    paid_date = Column(Date)
    
    # Payment details
    payment_method = Column(String(50))
    payment_reference = Column(String(100))
    
    # Notes
    notes = Column(String(2000))
    terms_and_conditions = Column(String(2000))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="invoices")
    project = relationship("Project", back_populates="invoices")

    def __repr__(self):
        return f"<Invoice(id={self.id}, invoice_number={self.invoice_number}, status={self.status}, amount={self.amount})>"

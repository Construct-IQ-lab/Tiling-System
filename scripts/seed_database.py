#!/usr/bin/env python3
"""
Seed script to populate database with test data for multi-tenant system.
Creates:
- 1 admin user
- 2 test companies with different branding
- Company owners and staff for each company
- Sample projects for each company
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid

from database import SessionLocal, Base, engine
from models.company import Company, CompanyStatus
from models.user import User, UserRole
from models.project import Project, ProjectStatus
from models.quote import Quote, QuoteStatus
from models.invoice import Invoice, InvoiceStatus
from services.auth_service import get_password_hash


def create_seed_data():
    """Create seed data for testing"""
    
    # Create tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_admin = db.query(User).filter(User.email == "admin@tilingsystem.com").first()
        if existing_admin:
            print("⚠️  Seed data already exists. Skipping...")
            return
        
        print("\n🌱 Creating seed data...\n")
        
        # Create admin user
        print("Creating admin user...")
        admin_user = User(
            id=str(uuid.uuid4()),
            email="admin@tilingsystem.com",
            password_hash=get_password_hash("admin123"),
            first_name="System",
            last_name="Admin",
            role=UserRole.admin,
            company_id=None,
            is_active=True
        )
        db.add(admin_user)
        print(f"  ✓ Admin: {admin_user.email} / admin123")
        
        # Create Company 1: Elite Tiling Solutions
        print("\nCreating Company 1: Elite Tiling Solutions...")
        company1 = Company(
            id=str(uuid.uuid4()),
            name="Elite Tiling Solutions",
            slug="elitetilingsolutions",
            email="contact@elitetiling.com",
            phone="+1-555-0100",
            address="123 Main St, New York, NY 10001",
            logo_url=None,
            primary_color="#1a73e8",
            secondary_color="#34a853",
            status=CompanyStatus.active,
            subscription_plan="professional"
        )
        db.add(company1)
        print(f"  ✓ Company: {company1.name} (/{company1.slug})")
        
        # Create users for Company 1
        company1_owner = User(
            id=str(uuid.uuid4()),
            email="owner@elitetiling.com",
            password_hash=get_password_hash("owner123"),
            first_name="John",
            last_name="Smith",
            role=UserRole.company_owner,
            company_id=company1.id,
            is_active=True
        )
        db.add(company1_owner)
        print(f"  ✓ Owner: {company1_owner.email} / owner123")
        
        company1_staff = User(
            id=str(uuid.uuid4()),
            email="staff@elitetiling.com",
            password_hash=get_password_hash("staff123"),
            first_name="Jane",
            last_name="Doe",
            role=UserRole.company_staff,
            company_id=company1.id,
            is_active=True
        )
        db.add(company1_staff)
        print(f"  ✓ Staff: {company1_staff.email} / staff123")
        
        # Create projects for Company 1
        project1 = Project(
            id=str(uuid.uuid4()),
            name="Residential Kitchen Renovation",
            description="Complete kitchen tiling project for residential client",
            company_id=company1.id,
            created_by=company1_owner.id,
            client_name="Robert Johnson",
            client_email="robert.j@email.com",
            client_phone="+1-555-0201",
            status=ProjectStatus.in_progress,
            budget=5500.00,
            measurements={"length": 8, "width": 6, "unit": "meters"},
            tiles={"type": "Ceramic", "size": "30x30cm"},
            materials={"tiles": 180, "grout_kg": 4.5, "adhesive_bags": 3}
        )
        db.add(project1)
        
        project2 = Project(
            id=str(uuid.uuid4()),
            name="Commercial Bathroom Tiling",
            description="Office building bathroom renovation",
            company_id=company1.id,
            created_by=company1_staff.id,
            client_name="ABC Corp",
            client_email="facilities@abccorp.com",
            status=ProjectStatus.planning,
            budget=12000.00
        )
        db.add(project2)
        print(f"  ✓ Created 2 sample projects")
        
        # Create Company 2: Pro Tile Masters
        print("\nCreating Company 2: Pro Tile Masters...")
        company2 = Company(
            id=str(uuid.uuid4()),
            name="Pro Tile Masters",
            slug="protilemasters",
            email="info@protilemasters.com",
            phone="+1-555-0300",
            address="456 Oak Ave, Los Angeles, CA 90001",
            logo_url=None,
            primary_color="#9c27b0",
            secondary_color="#ff9800",
            status=CompanyStatus.active,
            subscription_plan="basic"
        )
        db.add(company2)
        print(f"  ✓ Company: {company2.name} (/{company2.slug})")
        
        # Create users for Company 2
        company2_owner = User(
            id=str(uuid.uuid4()),
            email="owner@protilemasters.com",
            password_hash=get_password_hash("owner123"),
            first_name="Maria",
            last_name="Garcia",
            role=UserRole.company_owner,
            company_id=company2.id,
            is_active=True
        )
        db.add(company2_owner)
        print(f"  ✓ Owner: {company2_owner.email} / owner123")
        
        # Create project for Company 2
        project3 = Project(
            id=str(uuid.uuid4()),
            name="Hotel Lobby Floor Tiling",
            description="Luxury hotel entrance tiling with marble",
            company_id=company2.id,
            created_by=company2_owner.id,
            client_name="Grand Hotel Group",
            client_email="projects@grandhotel.com",
            status=ProjectStatus.completed,
            budget=25000.00,
            measurements={"length": 15, "width": 10, "unit": "meters"}
        )
        db.add(project3)
        print(f"  ✓ Created 1 sample project")
        
        # Create quotes
        print("\nCreating sample quotes...")
        quote1 = Quote(
            id=str(uuid.uuid4()),
            quote_number=f"QT-{datetime.utcnow().strftime('%Y%m%d')}-SEED001",
            company_id=company1.id,
            project_id=project1.id,
            client_name="Robert Johnson",
            client_email="robert.j@email.com",
            total_amount=5500.00,
            status=QuoteStatus.approved,
            valid_until=datetime.utcnow() + timedelta(days=30)
        )
        db.add(quote1)
        print(f"  ✓ Created quote for Elite Tiling Solutions")
        
        # Create invoices
        print("\nCreating sample invoices...")
        invoice1 = Invoice(
            id=str(uuid.uuid4()),
            invoice_number=f"INV-{datetime.utcnow().strftime('%Y%m%d')}-001",
            company_id=company2.id,
            project_id=project3.id,
            amount=25000.00,
            status=InvoiceStatus.paid,
            due_date=datetime.utcnow() + timedelta(days=30),
            paid_date=datetime.utcnow()
        )
        db.add(invoice1)
        print(f"  ✓ Created invoice for Pro Tile Masters")
        
        # Commit all changes
        db.commit()
        
        print("\n" + "="*60)
        print("✅ Seed data created successfully!")
        print("="*60)
        print("\n📋 Test Credentials:\n")
        print("Admin Portal:")
        print("  Email: admin@tilingsystem.com")
        print("  Password: admin123")
        print("  URL: http://localhost:8000/frontend/admin/index.html")
        print("\nCompany 1 - Elite Tiling Solutions:")
        print("  Owner: owner@elitetiling.com / owner123")
        print("  Staff: staff@elitetiling.com / staff123")
        print("  URL: http://localhost:8000/frontend/company/index.html?slug=elitetilingsolutions")
        print("\nCompany 2 - Pro Tile Masters:")
        print("  Owner: owner@protilemasters.com / owner123")
        print("  URL: http://localhost:8000/frontend/company/index.html?slug=protilemasters")
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error creating seed data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_seed_data()

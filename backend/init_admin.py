#!/usr/bin/env python3
"""
Database initialization script to create the initial admin user.
Run this script after the database has been initialized.
"""

from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models.user import User, UserRole
from services.auth_service import AuthService


def create_admin_user(db: Session):
    """
    Create the initial admin user if it doesn't exist.
    """
    # Check if admin user already exists
    admin_email = "admin@tilingsystem.com"
    existing_admin = db.query(User).filter(User.email == admin_email).first()
    
    if existing_admin:
        print(f"✓ Admin user already exists: {admin_email}")
        print(f"  Role: {existing_admin.role}")
        print(f"  Active: {existing_admin.is_active}")
        return existing_admin
    
    # Create new admin user
    admin_password = "admin123"
    password_hash = AuthService.get_password_hash(admin_password)
    
    admin_user = User(
        email=admin_email,
        password_hash=password_hash,
        first_name="System",
        last_name="Administrator",
        role=UserRole.ADMIN,
        company_id=None,  # Admin users are not associated with a company
        is_active=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print("\n" + "="*60)
    print("✓ Initial admin user created successfully!")
    print("="*60)
    print(f"\nAdmin Credentials:")
    print(f"  Email:    {admin_email}")
    print(f"  Password: {admin_password}")
    print(f"\n⚠️  IMPORTANT: Please change the password after first login!")
    print("="*60 + "\n")
    
    return admin_user


def main():
    """
    Main function to initialize the database and create admin user.
    """
    print("\n" + "="*60)
    print("Tiling System - Database Initialization")
    print("="*60 + "\n")
    
    # Initialize database tables
    print("Step 1: Initializing database tables...")
    try:
        init_db()
        print("✓ Database tables initialized successfully!\n")
    except Exception as e:
        print(f"✗ Error initializing database: {e}\n")
        return
    
    # Create admin user
    print("Step 2: Creating admin user...")
    db = SessionLocal()
    try:
        create_admin_user(db)
    except Exception as e:
        print(f"✗ Error creating admin user: {e}\n")
        db.rollback()
    finally:
        db.close()
    
    print("Database initialization complete!\n")


if __name__ == "__main__":
    main()

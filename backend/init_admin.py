#!/usr/bin/env python3
"""
Admin Initialization Script

This script creates the first admin user for the Tiling System.
It checks if an admin user already exists and creates one if not.

Usage:
    python init_admin.py
"""

from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models.user import User, UserRole
from services.auth_service import AuthService


def create_admin_user(db: Session):
    """
    Create the default admin user if it doesn't exist.
    
    Args:
        db: Database session
    """
    admin_email = "admin@tilingsystem.com"
    admin_password = "admin123"
    
    # Check if admin user already exists
    existing_admin = db.query(User).filter(User.email == admin_email).first()
    
    if existing_admin:
        print(f"✓ Admin user already exists: {admin_email}")
        print(f"  Role: {existing_admin.role}")
        print(f"  Active: {existing_admin.is_active}")
        return existing_admin
    
    # Create new admin user
    print(f"Creating admin user: {admin_email}")
    
    admin_user = User(
        email=admin_email,
        password_hash=AuthService.get_password_hash(admin_password),
        first_name="System",
        last_name="Administrator",
        role=UserRole.ADMIN,
        company_id=None,  # Admin users don't belong to any company
        is_active=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print(f"\n✓ Admin user created successfully!")
    print(f"\n{'='*60}")
    print(f"  Admin Credentials:")
    print(f"{'='*60}")
    print(f"  Email:    {admin_email}")
    print(f"  Password: {admin_password}")
    print(f"{'='*60}")
    print(f"\n⚠️  IMPORTANT: Change the password after first login!")
    print(f"\n")
    
    return admin_user


def main():
    """
    Main function to initialize the database and create admin user.
    """
    print("="*60)
    print("  Tiling System - Admin Initialization")
    print("="*60)
    print()
    
    # Initialize database (create tables if they don't exist)
    print("Initializing database...")
    try:
        init_db()
        print("✓ Database initialized successfully\n")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        return
    
    # Create admin user
    db = SessionLocal()
    try:
        create_admin_user(db)
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("Admin initialization complete!")


if __name__ == "__main__":
    main()

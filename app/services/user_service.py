"""
User service for business logic.

This module contains the business logic for user-related operations,
sitting between the API layer (routers) and the data access layer (repositories).
It handles validation, coordination, and error handling.
"""

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from app.schemas.user import UserCreate
from app.utils.password import hash_password


def register_user(db: Session, user_data: UserCreate) -> User:
    """
    Register a new user with validation and error handling.
    
    This function orchestrates the user registration process:
    1. Checks if username already exists
    2. Checks if email already exists
    3. Hashes the password
    4. Creates the user in the database
    5. Handles any database errors
    
    Args:
        db: Database session
        user_data: Validated user registration data (UserCreate schema)
        
    Returns:
        The created User model instance
        
    Raises:
        HTTPException 400: If username or email already exists
        HTTPException 500: If an unexpected database error occurs
        
    Example:
        >>> from app.schemas.user import UserCreate
        >>> user_data = UserCreate(
        ...     username="john_doe",
        ...     email="john@example.com",
        ...     password="SecurePass123"
        ... )
        >>> user = register_user(db, user_data)
        >>> print(user.username)
        john_doe
    """
    # Check if username already exists
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    password_hash = hash_password(user_data.password)
    
    # Create the user
    try:
        user = create_user(
            db=db,
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash
        )
        return user
    except IntegrityError as e:
        # This shouldn't happen if our checks above work, but it's a safety net
        # for race conditions or database-level constraint violations
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    except Exception as e:
        # Catch any other unexpected errors
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        )


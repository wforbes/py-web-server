"""
User repository for database operations.

This module provides the data access layer for user-related database operations,
abstracting SQLAlchemy queries and following the repository pattern for better
separation of concerns and easier testing.
"""

from typing import Optional

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.models.user import User


def create_user(
    db: Session,
    username: str,
    email: str,
    password_hash: str
) -> User:
    """
    Create a new user in the database.
    
    This function creates and persists a new user with the provided credentials.
    The User model will automatically generate the ID and timestamps.
    
    Args:
        db: Database session
        username: Unique username
        email: Unique email address
        password_hash: Hashed password (use hash_password() utility)
        
    Returns:
        The created User model instance
        
    Raises:
        IntegrityError: If username or email already exists (unique constraint violation)
        
    Example:
        >>> from app.utils.password import hash_password
        >>> user = create_user(db, "john_doe", "john@example.com", hash_password("password"))
        >>> print(user.username)
        john_doe
    """
    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)  # Refresh to get generated id and timestamps
    
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by email address.
    
    Uses SQLAlchemy 2.0 select() syntax for querying.
    
    Args:
        db: Database session
        email: Email address to search for
        
    Returns:
        User model if found, None otherwise
        
    Example:
        >>> user = get_user_by_email(db, "john@example.com")
        >>> if user:
        ...     print(user.username)
    """
    stmt = select(User).where(User.email == email)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Retrieve a user by username.
    
    Uses SQLAlchemy 2.0 select() syntax for querying.
    
    Args:
        db: Database session
        username: Username to search for
        
    Returns:
        User model if found, None otherwise
        
    Example:
        >>> user = get_user_by_username(db, "john_doe")
        >>> if user:
        ...     print(user.email)
    """
    stmt = select(User).where(User.username == username)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def get_user_by_email_or_username(
    db: Session,
    identifier: str
) -> Optional[User]:
    """
    Retrieve a user by either email or username.
    
    This is useful for login flows where the user can provide either
    their email or username. Uses SQLAlchemy's or_() for the query.
    
    Args:
        db: Database session
        identifier: Email address or username to search for
        
    Returns:
        User model if found, None otherwise
        
    Example:
        >>> # Can login with either
        >>> user = get_user_by_email_or_username(db, "john@example.com")
        >>> user = get_user_by_email_or_username(db, "john_doe")
    """
    stmt = select(User).where(
        or_(
            User.email == identifier,
            User.username == identifier
        )
    )
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """
    Retrieve a user by their ID.
    
    Args:
        db: Database session
        user_id: User's UUID as string
        
    Returns:
        User model if found, None otherwise
        
    Example:
        >>> user = get_user_by_id(db, "550e8400-e29b-41d4-a716-446655440000")
    """
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


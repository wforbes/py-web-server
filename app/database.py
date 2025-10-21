"""
Database connection and session management using SQLAlchemy 2.0.

This module sets up the database engine, session factory, and provides
the Base class for ORM models. It also includes a FastAPI dependency
for database session injection.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


# Create SQLAlchemy engine
# For production with connection pooling, you might want to add:
# pool_pre_ping=True, pool_size=5, max_overflow=10
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries when debug mode is enabled
)

# Create session factory
# autocommit=False: Don't automatically commit after each operation
# autoflush=False: Don't automatically flush before queries
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Base class for all ORM models
class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    
    All models should inherit from this class to be properly
    registered with SQLAlchemy's declarative system.
    """
    pass


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.
    
    This function creates a new SQLAlchemy session for each request
    and ensures it's properly closed after the request is completed.
    
    Usage in route handlers:
        @router.get("/users")
        def get_users(db: Session = Depends(get_db)):
            # Use db session here
            pass
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


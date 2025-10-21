"""
Pydantic schemas for user-related requests and responses.

This module defines the data validation and serialization schemas
for user operations, including registration and user information display.
"""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    """
    Schema for user registration/creation.
    
    Used for POST /auth/signup endpoint to validate incoming user data.
    Passwords must meet strength requirements.
    """
    
    username: Annotated[str, Field(
        min_length=3,
        max_length=50,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Username (3-50 chars, alphanumeric, underscore, hyphen only)"
    )]
    
    email: Annotated[EmailStr, Field(
        description="Valid email address"
    )]
    
    password: Annotated[str, Field(
        min_length=8,
        max_length=100,
        description="Password (minimum 8 characters)"
    )]
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password meets strength requirements.
        
        Requirements:
        - At least 8 characters (enforced by Field)
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        
        Args:
            v: The password string to validate
            
        Returns:
            The validated password
            
        Raises:
            ValueError: If password doesn't meet requirements
        """
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        
        return v
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """
        Additional username validation.
        
        Ensures username doesn't contain only special characters.
        
        Args:
            v: The username string to validate
            
        Returns:
            The validated username
            
        Raises:
            ValueError: If username is invalid
        """
        if not any(c.isalnum() for c in v):
            raise ValueError('Username must contain at least one alphanumeric character')
        
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "john_doe",
                    "email": "john.doe@example.com",
                    "password": "SecurePass123"
                }
            ]
        }
    }


class UserResponse(BaseModel):
    """
    Schema for user information in API responses.
    
    Used to serialize user data without exposing sensitive information
    like password hashes. This is returned after signup, login, and
    when fetching user information.
    """
    
    id: str
    username: str
    email: EmailStr
    created_at: datetime
    
    model_config = {
        "from_attributes": True,  # Allows creation from SQLAlchemy models
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "username": "john_doe",
                    "email": "john.doe@example.com",
                    "created_at": "2025-10-21T12:00:00Z"
                }
            ]
        }
    }


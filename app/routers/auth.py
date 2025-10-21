"""
Authentication routes for user signup, login, and token management.

This module defines all authentication-related API endpoints including
user registration, login, token refresh, and current user retrieval.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import register_user


# Create the authentication router
router = APIRouter()


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with username, email, and password. "
                "Username and email must be unique. Password must meet strength requirements.",
    responses={
        201: {
            "description": "User successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "username": "john_doe",
                        "email": "john@example.com",
                        "created_at": "2025-10-21T12:00:00Z"
                    }
                }
            }
        },
        400: {
            "description": "Bad request - validation error or duplicate username/email",
            "content": {
                "application/json": {
                    "examples": {
                        "duplicate_username": {
                            "summary": "Duplicate username",
                            "value": {"detail": "Username already registered"}
                        },
                        "duplicate_email": {
                            "summary": "Duplicate email",
                            "value": {"detail": "Email already registered"}
                        },
                        "validation_error": {
                            "summary": "Validation error",
                            "value": {
                                "detail": [
                                    {
                                        "loc": ["body", "password"],
                                        "msg": "Password must contain at least one uppercase letter",
                                        "type": "value_error"
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation error - invalid input format"
        }
    }
)
def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Register a new user account.
    
    This endpoint handles user registration by:
    1. Validating the input data (Pydantic validation)
    2. Checking for duplicate username/email
    3. Hashing the password securely
    4. Creating the user in the database
    5. Returning the created user information (without password)
    
    Args:
        user_data: User registration data (username, email, password)
        db: Database session (injected by FastAPI)
        
    Returns:
        UserResponse: The created user's information
        
    Raises:
        HTTPException 400: If username or email already exists
        HTTPException 422: If validation fails
    """
    user = register_user(db, user_data)
    return UserResponse.model_validate(user)



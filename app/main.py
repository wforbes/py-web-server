"""
FastAPI application entry point.

This module initializes the FastAPI application, configures middleware,
and registers all route handlers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

# Initialize FastAPI application
app = FastAPI(
    title=settings.project_name,
    description="A modern web API with JWT authentication and PostgreSQL database",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """
    Health check endpoint.
    
    Returns a simple status message to verify the API is running.
    This endpoint is useful for monitoring, load balancers, and deployment checks.
    
    Returns:
        dict: Status message indicating the API is healthy
    """
    return {"status": "healthy"}


# Router registration will be added here as we build features
# Example:
# from app.routers import auth
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


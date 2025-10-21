"""
Application configuration management using pydantic-settings.

This module loads environment variables from .env file and provides
type-safe configuration throughout the application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Automatically loads from .env file in the project root.
    All values can be overridden by environment variables.
    """
    
    # Database Configuration
    database_url: str
    
    # JWT Configuration
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    refresh_token_expire_minutes: int = 1440  # 24 hours
    
    # CORS Configuration
    cors_origins: str  # Comma-separated list of origins
    
    # Application Configuration
    project_name: str = "Python Web Server API"
    debug: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """
        Parse CORS origins from comma-separated string to list.
        
        Returns:
            List of allowed CORS origins
        """
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
# This will be instantiated once when the module is imported
settings = Settings()


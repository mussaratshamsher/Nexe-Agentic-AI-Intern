import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings managed by Pydantic-Settings.
    Loads environment variables from a .env file and validates them.
    """
    model_config = SettingsConfigDict(
        env_file='.env',              # Load environment variables from .env file
        env_file_encoding='utf-8',
        extra='ignore'                 # Ignore any extra environment variables
    )

    # Application
    app_name: str = "AI Business Operations Manager"
    api_v1_str: str = "/api/v1"
    debug: bool = False
    secret_key: str

    # OpenAI
    openai_api_key: str
    openai_org_id: Optional[str] = None

    # Supabase
    supabase_url: str
    supabase_key: str # Anon key for client-side use (if needed)
    supabase_service_role_key: str # For backend operations

    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_DAYS: int = 7

    # Database
    # Example format: postgresql+asyncpg://user:password@host:port/database
    database_url: str

    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Sentry (optional)
    sentry_dsn: Optional[str] = None

    # Email (mocked initially, but good to have config)
    # email_use_tls: bool = True
    # email_port: int = 587
    # email_host: str = "smtp.example.com"
    # email_host_user: str = "noreply@yourdomain.com"
    # email_host_password: str = "your_email_password" # Use environment variables for sensitive data
    # email_sender: str = "noreply@yourdomain.com"

# Singleton instance of settings
# This ensures settings are loaded only once and are globally accessible.
# However, it's generally better practice to inject settings where needed.
# For simplicity, we'll create it here, but consider dependency injection later.
settings = Settings()


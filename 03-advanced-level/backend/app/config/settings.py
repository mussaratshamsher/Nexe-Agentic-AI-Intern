from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    GROQ_API_KEY: str
    DATABASE_URL: str
    JWT_SECRET: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Phase 4 Integrations
    GMAIL_CREDENTIALS_PATH: str = "credentials.json"
    GMAIL_TOKEN_PATH: str = "token.json"
    GMAIL_CREDENTIALS_JSON: Optional[str] = None
    GMAIL_TOKEN_JSON: Optional[str] = None
    
    # WhatsApp - Ultramsg
    ULTRAMSG_INSTANCE_ID: Optional[str] = None
    ULTRAMSG_TOKEN: Optional[str] = None
    
    # WhatsApp - Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_SANDBOX_NUMBER: Optional[str] = None
    FROM_PHONE_NUMBER: Optional[str] = None
    TO_PHONE_NUMBER: Optional[str] = None

    @property
    def MY_PHONE_NUMBER(self) -> Optional[str]:
        return self.TO_PHONE_NUMBER

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

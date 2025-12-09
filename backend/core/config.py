"""
Configuration settings for the application
"""

from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Smart Revenue Leakage Advisor"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS - Allow all origins for development
    ALLOWED_ORIGINS: str = "*"
    
    # Database
    DATABASE_URL: str = "sqlite:///./revenue_advisor.db"
    
    # OpenAI API (for AI-powered analysis)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
    OPENAI_MODEL_NAME: str = "gpt-4o-mini"
    
    # JWT Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production-min-32-chars")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Business Analysis Thresholds
    HIGH_RISK_THRESHOLD: float = 75.0
    MEDIUM_RISK_THRESHOLD: float = 50.0
    LOW_RISK_THRESHOLD: float = 25.0
    
    # Revenue Leakage Thresholds (%)
    CRITICAL_LEAKAGE: float = 20.0
    HIGH_LEAKAGE: float = 10.0
    MODERATE_LEAKAGE: float = 5.0
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list[str] = [".csv", ".xlsx", ".xls"]
    UPLOAD_DIR: str = "uploads"
    REPORT_DIR: str = "reports"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

"""
Database configuration and initialization
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

from core.config import settings

# Create database directory if it doesn't exist
os.makedirs("database", exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.REPORT_DIR, exist_ok=True)

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Database Models
class User(Base):
    """User authentication and profile"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    company_name = Column(String)
    role = Column(String)  # Finance Manager, Business Analyst, etc.
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class BusinessAnalysis(Base):
    """Store business analysis records"""
    __tablename__ = "business_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, unique=True, index=True)
    business_name = Column(String, index=True)
    business_stage = Column(String)  # new or existing
    business_model = Column(String)
    industry = Column(String)
    
    # Analysis results (stored as JSON)
    form_data = Column(JSON)
    revenue_analysis = Column(JSON)
    recovery_strategy = Column(JSON)
    leakage_points = Column(JSON)
    
    # Metrics
    total_revenue = Column(Float)
    leakage_amount = Column(Float)
    leakage_percentage = Column(Float)
    risk_score = Column(Float)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class Report(Base):
    """Store generated reports"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String, unique=True, index=True)
    analysis_id = Column(String, index=True)
    user_id = Column(Integer, index=True)
    
    title = Column(String)
    description = Column(Text)
    category = Column(String)
    date_range = Column(String)
    
    file_path = Column(String)
    file_format = Column(String)
    file_size = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class UploadedData(Base):
    """Store uploaded CSV/Excel files and parsed data"""
    __tablename__ = "uploaded_data"
    
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, index=True)
    
    file_name = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)
    file_type = Column(String)  # csv, xlsx, xls
    
    # Column mapping
    column_mapping = Column(JSON)  # Maps user columns to system fields
    
    # Parsed data statistics
    total_rows = Column(Integer)
    total_columns = Column(Integer)
    data_summary = Column(JSON)  # Statistics about the data
    
    # Analysis results
    leakage_data = Column(JSON)  # Detected leakages
    
    status = Column(String, default="processing")  # processing, completed, failed
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    """Store user-configured alerts"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, index=True)
    
    name = Column(String, nullable=False)
    description = Column(Text)
    
    # Alert configuration
    metric = Column(String)  # revenue_drop, high_leakage, etc.
    condition = Column(String)  # greater_than, less_than, equals
    threshold = Column(Float)
    severity = Column(String)  # low, medium, high, critical
    
    # Notification settings
    notify_email = Column(Boolean, default=True)
    notify_in_app = Column(Boolean, default=True)
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Notification(Base):
    """Store in-app notifications"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, index=True)
    
    title = Column(String, nullable=False)
    message = Column(Text)
    severity = Column(String)  # info, warning, error, success
    
    is_read = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

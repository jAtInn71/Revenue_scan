"""
Settings API routes - User profile and preferences
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from database.database import get_db, User
from services.auth_service import get_current_user, get_password_hash, verify_password

router = APIRouter()

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class PreferencesUpdate(BaseModel):
    currency: Optional[str] = None
    date_format: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None

@router.get("/profile")
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get user profile
    """
    return {
        "email": current_user.email,
        "fullName": current_user.full_name,
        "companyName": current_user.company_name,
        "role": current_user.role,
        "createdAt": current_user.created_at.isoformat(),
        "lastLogin": current_user.last_login.isoformat() if current_user.last_login else None
    }

@router.put("/profile")
async def update_profile(
    update_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile
    """
    if update_data.full_name is not None:
        current_user.full_name = update_data.full_name
    if update_data.company_name is not None:
        current_user.company_name = update_data.company_name
    if update_data.role is not None:
        current_user.role = update_data.role
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Profile updated successfully",
        "profile": {
            "email": current_user.email,
            "fullName": current_user.full_name,
            "companyName": current_user.company_name,
            "role": current_user.role
        }
    }

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    """
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}

@router.get("/preferences")
async def get_preferences(
    current_user: User = Depends(get_current_user)
):
    """
    Get user preferences (mock data for now)
    """
    return {
        "currency": "USD",
        "dateFormat": "MM/DD/YYYY",
        "timezone": "America/New_York",
        "language": "en",
        "notifications": {
            "email": True,
            "inApp": True,
            "weeklyReport": True
        }
    }

@router.put("/preferences")
async def update_preferences(
    preferences: PreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user preferences
    """
    # For now, just return success
    # In production, store preferences in database
    return {
        "message": "Preferences updated successfully",
        "preferences": {
            "currency": preferences.currency or "USD",
            "dateFormat": preferences.date_format or "MM/DD/YYYY",
            "timezone": preferences.timezone or "America/New_York",
            "language": preferences.language or "en"
        }
    }

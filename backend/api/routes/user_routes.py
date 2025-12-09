"""
User Management API routes - Admin only
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from database.database import get_db, User, BusinessAnalysis, UploadedData
from services.auth_service import get_current_user

router = APIRouter()

# Pydantic Models
class UserListResponse(BaseModel):
    id: int
    email: str
    full_name: str
    company_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class UserDetailResponse(BaseModel):
    id: int
    email: str
    full_name: str
    company_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    total_analyses: int
    total_uploads: int
    
class UpdateUserRoleRequest(BaseModel):
    role: str

def verify_admin(current_user: User):
    """Verify that the current user is an admin"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.get("/users", response_model=List[UserListResponse])
async def get_all_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all users - Admin only
    """
    verify_admin(current_user)
    
    users = db.query(User).order_by(User.created_at.desc()).all()
    return users

@router.get("/users/{user_id}", response_model=UserDetailResponse)
async def get_user_details(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed user information including their data - Admin only
    """
    verify_admin(current_user)
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's analyses count
    total_analyses = db.query(BusinessAnalysis).filter(
        BusinessAnalysis.user_id == user_id
    ).count()
    
    # Get user's uploads count
    total_uploads = db.query(UploadedData).filter(
        UploadedData.user_id == user_id
    ).count()
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "company_name": user.company_name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "last_login": user.last_login,
        "total_analyses": total_analyses,
        "total_uploads": total_uploads
    }

@router.get("/users/{user_id}/analyses")
async def get_user_analyses(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all analyses created by a specific user - Admin only
    """
    verify_admin(current_user)
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    analyses = db.query(BusinessAnalysis).filter(
        BusinessAnalysis.user_id == user_id
    ).order_by(BusinessAnalysis.created_at.desc()).all()
    
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        },
        "total": len(analyses),
        "analyses": [
            {
                "id": analysis.id,
                "analysis_id": analysis.analysis_id,
                "business_name": analysis.business_name,
                "business_stage": analysis.business_stage,
                "business_model": analysis.business_model,
                "industry": analysis.industry,
                "total_revenue": analysis.total_revenue,
                "leakage_amount": analysis.leakage_amount,
                "leakage_percentage": analysis.leakage_percentage,
                "risk_score": analysis.risk_score,
                "created_at": analysis.created_at
            }
            for analysis in analyses
        ]
    }

@router.get("/users/{user_id}/uploads")
async def get_user_uploads(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all uploads by a specific user - Admin only
    """
    verify_admin(current_user)
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    uploads = db.query(UploadedData).filter(
        UploadedData.user_id == user_id
    ).order_by(UploadedData.created_at.desc()).all()
    
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        },
        "total": len(uploads),
        "uploads": [
            {
                "id": upload.id,
                "upload_id": upload.upload_id,
                "filename": upload.filename,
                "file_type": upload.file_type,
                "rows_count": upload.rows_count,
                "columns_count": upload.columns_count,
                "created_at": upload.created_at
            }
            for upload in uploads
        ]
    }

@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    request: UpdateUserRoleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user role - Admin only
    """
    verify_admin(current_user)
    
    # Validate role
    if request.role not in ["admin", "user"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be either 'admin' or 'user'"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent self-demotion
    if user.id == current_user.id and request.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot change your own admin role"
        )
    
    user.role = request.role
    db.commit()
    db.refresh(user)
    
    return {
        "message": "User role updated successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    }

@router.put("/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Activate/deactivate user - Admin only
    """
    verify_admin(current_user)
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent self-deactivation
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate your own account"
        )
    
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    
    return {
        "message": f"User {'activated' if user.is_active else 'deactivated'} successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active
        }
    }

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete user - Admin only
    """
    verify_admin(current_user)
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent self-deletion
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own account"
        )
    
    db.delete(user)
    db.commit()
    
    return {
        "message": "User deleted successfully"
    }

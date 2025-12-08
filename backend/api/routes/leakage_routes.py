"""
Leakage Analysis Explorer API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import random

from database.database import get_db, User, UploadedData, BusinessAnalysis
from services.auth_service import get_current_user

router = APIRouter()

@router.get("/leakage")
async def get_leakage_data(
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get leakage analysis data with filters
    """
    # Get leakage data from uploads
    uploads = db.query(UploadedData).filter(
        UploadedData.user_id == current_user.id,
        UploadedData.status == "completed"
    ).all()
    
    all_leakages = []
    for upload in uploads:
        if upload.leakage_data and "items" in upload.leakage_data:
            for item in upload.leakage_data["items"]:
                # Apply filters
                if status and item.get("status") != status:
                    continue
                if severity and item.get("severity") != severity:
                    continue
                if category and item.get("category") != category:
                    continue
                
                all_leakages.append({
                    **item,
                    "source": upload.file_name,
                    "upload_id": upload.upload_id,
                    "detected_at": upload.created_at.isoformat()
                })
    
    return {
        "total": len(all_leakages),
        "items": all_leakages
    }

@router.get("/leakage/{leakage_id}")
async def get_leakage_detail(
    leakage_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific leakage
    """
    # Search through uploads for the leakage
    uploads = db.query(UploadedData).filter(
        UploadedData.user_id == current_user.id
    ).all()
    
    for upload in uploads:
        if upload.leakage_data and "items" in upload.leakage_data:
            for item in upload.leakage_data["items"]:
                if item.get("id") == leakage_id:
                    return {
                        **item,
                        "source": upload.file_name,
                        "upload_id": upload.upload_id,
                        "detected_at": upload.created_at.isoformat(),
                        "recommendations": [
                            "Review transaction for accuracy",
                            "Implement validation checks",
                            "Set up alert for similar cases"
                        ],
                        "related_transactions": 3
                    }
    
    raise HTTPException(status_code=404, detail="Leakage not found")

@router.get("/leakage/export")
async def export_leakage_data(
    format: str = Query("csv", regex="^(csv|xlsx)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export leakage data to CSV or Excel
    """
    # For now, return a success message
    # In production, generate actual file
    return {
        "message": f"Export to {format.upper()} initiated",
        "download_url": f"/api/analysis/downloads/leakage_export_{datetime.now().strftime('%Y%m%d')}.{format}"
    }

@router.get("/summary")
async def get_analysis_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get summary of all analyses
    """
    analyses = db.query(BusinessAnalysis).filter(
        BusinessAnalysis.business_name == current_user.company_name
    ).all()
    
    uploads = db.query(UploadedData).filter(
        UploadedData.user_id == current_user.id,
        UploadedData.status == "completed"
    ).all()
    
    total_leakage = sum(a.leakage_amount for a in analyses if a.leakage_amount)
    
    # Count leakages from uploads
    upload_leakages = 0
    for upload in uploads:
        if upload.leakage_data:
            upload_leakages += len(upload.leakage_data.get("items", []))
    
    return {
        "totalAnalyses": len(analyses),
        "totalUploads": len(uploads),
        "totalLeakageAmount": float(total_leakage),
        "totalLeakageItems": upload_leakages,
        "avgRiskScore": sum(a.risk_score for a in analyses if a.risk_score) / len(analyses) if analyses else 0
    }

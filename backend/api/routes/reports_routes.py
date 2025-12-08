"""
Reports API routes - List and download reports
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
import os

from database.database import get_db, User, Report, BusinessAnalysis
from services.auth_service import get_current_user
from core.config import settings

router = APIRouter()

class ReportGenerateRequest(BaseModel):
    title: str
    category: str
    date_range: str
    analysis_id: Optional[str] = None

@router.get("/")
async def get_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all reports for current user
    """
    reports = db.query(Report).filter(
        Report.user_id == current_user.id
    ).order_by(Report.created_at.desc()).all()
    
    return [
        {
            "id": report.report_id,
            "title": report.title,
            "description": report.description,
            "category": report.category,
            "dateRange": report.date_range,
            "size": f"{report.file_size / 1024:.1f} KB" if report.file_size else "N/A",
            "format": report.file_format or "PDF",
            "createdAt": report.created_at.isoformat()
        }
        for report in reports
    ]

@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_report(
    request: ReportGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a new report
    """
    report_id = f"RPT-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
    
    # Create mock report file
    os.makedirs(settings.REPORT_DIR, exist_ok=True)
    file_path = os.path.join(settings.REPORT_DIR, f"{report_id}.pdf")
    
    # Create simple PDF placeholder
    with open(file_path, "wb") as f:
        f.write(b"%PDF-1.4\n%Mock Report File\n")
    
    file_size = os.path.getsize(file_path)
    
    new_report = Report(
        report_id=report_id,
        analysis_id=request.analysis_id,
        user_id=current_user.id,
        title=request.title,
        description=f"Revenue leakage analysis report for {request.date_range}",
        category=request.category,
        date_range=request.date_range,
        file_path=file_path,
        file_format="PDF",
        file_size=file_size
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    return {
        "report_id": new_report.report_id,
        "title": new_report.title,
        "message": "Report generated successfully"
    }

@router.get("/{report_id}/download")
async def download_report(
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download a specific report
    """
    report = db.query(Report).filter(
        Report.report_id == report_id,
        Report.user_id == current_user.id
    ).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if not os.path.exists(report.file_path):
        raise HTTPException(status_code=404, detail="Report file not found")
    
    return FileResponse(
        path=report.file_path,
        filename=f"{report.title.replace(' ', '_')}.pdf",
        media_type="application/pdf"
    )

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a report
    """
    report = db.query(Report).filter(
        Report.report_id == report_id,
        Report.user_id == current_user.id
    ).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Delete file if exists
    if os.path.exists(report.file_path):
        os.remove(report.file_path)
    
    db.delete(report)
    db.commit()
    
    return None

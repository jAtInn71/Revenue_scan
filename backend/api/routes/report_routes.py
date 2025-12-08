"""
API routes for report generation
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import os

from models.schemas import ReportRequest, ReportResponse
from database.database import get_db, BusinessAnalysis, Report
from services.report_service import ReportService
from core.config import settings

router = APIRouter()

# Ensure report directory exists
os.makedirs(settings.REPORT_DIR, exist_ok=True)

@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    request: ReportRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a comprehensive PDF report for an analysis
    """
    # Get analysis
    analysis = db.query(BusinessAnalysis).filter(
        BusinessAnalysis.analysis_id == request.analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {request.analysis_id} not found"
        )
    
    try:
        # Generate report
        report_service = ReportService()
        report_id = f"RPT-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        file_path = await report_service.generate_pdf_report(
            analysis=analysis,
            report_id=report_id,
            include_charts=request.include_charts,
            include_recommendations=request.include_recommendations
        )
        
        # Save report record
        file_size = os.path.getsize(file_path)
        db_report = Report(
            report_id=report_id,
            analysis_id=request.analysis_id,
            file_path=file_path,
            file_format=request.format,
            file_size=file_size
        )
        db.add(db_report)
        db.commit()
        
        # Return response
        return ReportResponse(
            report_id=report_id,
            download_url=f"/api/reports/download/{report_id}",
            generated_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )

@router.get("/download/{report_id}")
async def download_report(
    report_id: str,
    db: Session = Depends(get_db)
):
    """
    Download a generated report
    """
    report = db.query(Report).filter(Report.report_id == report_id).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report {report_id} not found"
        )
    
    if not os.path.exists(report.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found on server"
        )
    
    # Get business name for filename
    analysis = db.query(BusinessAnalysis).filter(
        BusinessAnalysis.analysis_id == report.analysis_id
    ).first()
    
    filename = f"Revenue_Report_{analysis.business_name.replace(' ', '_')}_{report_id}.pdf"
    
    return FileResponse(
        path=report.file_path,
        media_type="application/pdf",
        filename=filename
    )

@router.get("/list/{analysis_id}")
async def list_reports(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """
    List all reports for a specific analysis
    """
    reports = db.query(Report).filter(
        Report.analysis_id == analysis_id
    ).all()
    
    return [
        {
            "report_id": r.report_id,
            "file_format": r.file_format,
            "file_size": r.file_size,
            "created_at": r.created_at,
            "download_url": f"/api/reports/download/{r.report_id}"
        }
        for r in reports
    ]

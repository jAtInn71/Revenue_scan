"""
API routes for analysis operations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from database.database import get_db, BusinessAnalysis
from services.analysis_service import AnalysisService

router = APIRouter()

@router.get("/metrics/{analysis_id}")
async def get_analysis_metrics(
    analysis_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get key metrics and KPIs for a specific analysis
    """
    analysis = db.query(BusinessAnalysis).filter(
        BusinessAnalysis.analysis_id == analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {analysis_id} not found"
        )
    
    return {
        "analysis_id": analysis.analysis_id,
        "business_name": analysis.business_name,
        "metrics": {
            "total_revenue": analysis.total_revenue,
            "leakage_amount": analysis.leakage_amount,
            "leakage_percentage": analysis.leakage_percentage,
            "risk_score": analysis.risk_score,
            "recoverable_amount": analysis.revenue_analysis.get("recoverable_amount", 0)
        },
        "leakage_breakdown": [
            {
                "category": lp["category"],
                "estimated_loss": lp["estimated_loss"],
                "percentage": lp["percentage"],
                "severity": lp["severity"]
            }
            for lp in analysis.leakage_points
        ]
    }

@router.get("/compare")
async def compare_analyses(
    analysis_ids: str,  # comma-separated IDs
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Compare multiple analyses side by side
    """
    ids = [id.strip() for id in analysis_ids.split(",")]
    
    if len(ids) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least 2 analysis IDs required for comparison"
        )
    
    analyses = db.query(BusinessAnalysis).filter(
        BusinessAnalysis.analysis_id.in_(ids)
    ).all()
    
    if len(analyses) != len(ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more analyses not found"
        )
    
    comparison = {
        "analyses": [
            {
                "analysis_id": a.analysis_id,
                "business_name": a.business_name,
                "leakage_percentage": a.leakage_percentage,
                "risk_score": a.risk_score,
                "total_revenue": a.total_revenue,
                "leakage_amount": a.leakage_amount
            }
            for a in analyses
        ],
        "insights": {
            "highest_leakage": max(analyses, key=lambda a: a.leakage_percentage).business_name,
            "highest_risk": max(analyses, key=lambda a: a.risk_score).business_name,
            "average_leakage": sum(a.leakage_percentage for a in analyses) / len(analyses)
        }
    }
    
    return comparison

@router.get("/statistics")
async def get_statistics(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get overall platform statistics
    """
    total_analyses = db.query(BusinessAnalysis).count()
    
    if total_analyses == 0:
        return {
            "total_analyses": 0,
            "message": "No analyses performed yet"
        }
    
    analyses = db.query(BusinessAnalysis).all()
    
    total_leakage = sum(a.leakage_amount for a in analyses)
    avg_leakage_pct = sum(a.leakage_percentage for a in analyses) / total_analyses
    avg_risk_score = sum(a.risk_score for a in analyses) / total_analyses
    
    # Count by business stage
    new_business_count = sum(1 for a in analyses if a.business_stage == "new")
    existing_business_count = sum(1 for a in analyses if a.business_stage == "existing")
    
    # Industry distribution
    industries = {}
    for a in analyses:
        industries[a.industry] = industries.get(a.industry, 0) + 1
    
    return {
        "total_analyses": total_analyses,
        "new_businesses": new_business_count,
        "existing_businesses": existing_business_count,
        "total_leakage_detected": round(total_leakage, 2),
        "average_leakage_percentage": round(avg_leakage_pct, 2),
        "average_risk_score": round(avg_risk_score, 2),
        "industry_distribution": industries,
        "top_industries": sorted(industries.items(), key=lambda x: x[1], reverse=True)[:5]
    }

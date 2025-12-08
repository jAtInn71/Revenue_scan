"""
API routes for business operations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uuid

from models.schemas import (
    NewBusinessForm, 
    ExistingBusinessForm, 
    AnalysisResponse,
    BusinessStage
)
from database.database import get_db, BusinessAnalysis
from services.analysis_service import AnalysisService
from services.ai_service import AIService

router = APIRouter()

@router.post("/new/analyze", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def analyze_new_business(
    form: NewBusinessForm,
    db: Session = Depends(get_db)
):
    """
    Analyze a new business for potential revenue leakage risks
    Returns risk assessment and preventive recommendations
    """
    try:
        # Generate unique analysis ID
        analysis_id = f"ANAL-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        # Perform analysis
        analysis_service = AnalysisService()
        revenue_analysis = analysis_service.analyze_new_business(form)
        
        # Generate AI-powered recovery strategy
        ai_service = AIService()
        recovery_strategy = await ai_service.generate_new_business_strategy(form, revenue_analysis)
        executive_summary = await ai_service.generate_executive_summary(
            form.business_name,
            BusinessStage.NEW,
            revenue_analysis,
            recovery_strategy
        )
        
        # Save to database
        db_analysis = BusinessAnalysis(
            analysis_id=analysis_id,
            business_name=form.business_name,
            business_stage=BusinessStage.NEW,
            business_model=form.business_model,
            industry=form.industry,
            form_data=form.model_dump(),
            revenue_analysis=revenue_analysis.model_dump(),
            recovery_strategy=recovery_strategy.model_dump(),
            leakage_points=[lp.model_dump() for lp in revenue_analysis.leakage_points],
            total_revenue=revenue_analysis.total_revenue,
            leakage_amount=revenue_analysis.estimated_leakage_amount,
            leakage_percentage=revenue_analysis.leakage_percentage,
            risk_score=revenue_analysis.risk_assessment.overall_risk_score
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        # Prepare response
        response = AnalysisResponse(
            analysis_id=analysis_id,
            business_name=form.business_name,
            business_stage=BusinessStage.NEW,
            timestamp=datetime.now(),
            revenue_analysis=revenue_analysis,
            recovery_strategy=recovery_strategy,
            executive_summary=executive_summary
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@router.post("/existing/analyze", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def analyze_existing_business(
    form: ExistingBusinessForm,
    db: Session = Depends(get_db)
):
    """
    Analyze an existing business for revenue leakage
    Returns detected leaks and recovery recommendations
    """
    try:
        # Generate unique analysis ID
        analysis_id = f"ANAL-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        
        # Perform analysis
        analysis_service = AnalysisService()
        revenue_analysis = analysis_service.analyze_existing_business(form)
        
        # Generate AI-powered recovery strategy
        ai_service = AIService()
        recovery_strategy = await ai_service.generate_existing_business_strategy(form, revenue_analysis)
        executive_summary = await ai_service.generate_executive_summary(
            form.business_name,
            BusinessStage.EXISTING,
            revenue_analysis,
            recovery_strategy
        )
        
        # Save to database
        db_analysis = BusinessAnalysis(
            analysis_id=analysis_id,
            business_name=form.business_name,
            business_stage=BusinessStage.EXISTING,
            business_model=form.business_model,
            industry=form.industry,
            form_data=form.model_dump(),
            revenue_analysis=revenue_analysis.model_dump(),
            recovery_strategy=recovery_strategy.model_dump(),
            leakage_points=[lp.model_dump() for lp in revenue_analysis.leakage_points],
            total_revenue=revenue_analysis.total_revenue,
            leakage_amount=revenue_analysis.estimated_leakage_amount,
            leakage_percentage=revenue_analysis.leakage_percentage,
            risk_score=revenue_analysis.risk_assessment.overall_risk_score
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        # Prepare response
        response = AnalysisResponse(
            analysis_id=analysis_id,
            business_name=form.business_name,
            business_stage=BusinessStage.EXISTING,
            timestamp=datetime.now(),
            revenue_analysis=revenue_analysis,
            recovery_strategy=recovery_strategy,
            executive_summary=executive_summary
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@router.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a previously saved analysis by ID
    """
    analysis = db.query(BusinessAnalysis).filter(
        BusinessAnalysis.analysis_id == analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {analysis_id} not found"
        )
    
    # Reconstruct response from database
    from models.schemas import RevenueAnalysis, RecoveryStrategy
    
    response = AnalysisResponse(
        analysis_id=analysis.analysis_id,
        business_name=analysis.business_name,
        business_stage=analysis.business_stage,
        timestamp=analysis.created_at,
        revenue_analysis=RevenueAnalysis(**analysis.revenue_analysis),
        recovery_strategy=RecoveryStrategy(**analysis.recovery_strategy),
        executive_summary="Retrieved from database"
    )
    
    return response

@router.get("/analyses", response_model=List[dict])
async def list_analyses(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List all business analyses with pagination
    """
    analyses = db.query(BusinessAnalysis).offset(skip).limit(limit).all()
    
    return [
        {
            "analysis_id": a.analysis_id,
            "business_name": a.business_name,
            "business_stage": a.business_stage,
            "leakage_percentage": a.leakage_percentage,
            "risk_score": a.risk_score,
            "created_at": a.created_at
        }
        for a in analyses
    ]

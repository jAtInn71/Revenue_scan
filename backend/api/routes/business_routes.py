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
from database.database import get_db, BusinessAnalysis, User
from services.business_analysis_service import business_analysis_service
from services.auth_service import get_current_user

router = APIRouter()

@router.post("/new/analyze", status_code=status.HTTP_201_CREATED)
async def analyze_new_business(
    form: NewBusinessForm,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze a new business for potential revenue leakage risks
    Returns risk assessment and preventive recommendations
    """
    try:
        # Convert form to dict
        form_data = form.model_dump()
        
        # Perform analysis using business_analysis_service
        analysis_result = await business_analysis_service.analyze_new_business(form_data)
        
        # Save to database (optional - for history tracking)
        try:
            db_analysis = BusinessAnalysis(
                analysis_id=analysis_result['analysis_id'],
                business_name=form.business_name,
                business_stage=BusinessStage.NEW,
                business_model=form.business_model,
                industry=form.industry,
                form_data=form_data,
                revenue_analysis={},
                recovery_strategy={},
                leakage_points=analysis_result.get('leakage_points', []),
                total_revenue=analysis_result['financial_summary']['expected_monthly_revenue'],
                leakage_amount=analysis_result.get('total_potential_loss', 0),
                leakage_percentage=0,
                risk_score=0,
                user_id=current_user.id
            )
            db.add(db_analysis)
            db.commit()
        except Exception as db_error:
            print(f"Database save error (non-critical): {db_error}")
        
        # Return response
        return {
            "success": True,
            "analysis": analysis_result
        }
        
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
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

@router.post("/existing/analyze", status_code=status.HTTP_201_CREATED)
async def analyze_existing_business(
    form: ExistingBusinessForm,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze an existing business for revenue leakage
    Returns detected leaks and recovery recommendations
    """
    try:
        # Convert form to dict
        form_data = form.model_dump()
        
        # Perform analysis using business_analysis_service
        analysis_result = await business_analysis_service.analyze_existing_business(form_data)
        
        # Save to database (optional - for history tracking)
        try:
            db_analysis = BusinessAnalysis(
                analysis_id=analysis_result['analysis_id'],
                business_name=form.business_name,
                business_stage=BusinessStage.EXISTING,
                business_model=form.business_model,
                industry=form.industry,
                form_data=form_data,
                revenue_analysis={},
                recovery_strategy={},
                leakage_points=analysis_result.get('leakage_points', []),
                total_revenue=analysis_result['financial_summary']['monthly_revenue'],
                leakage_amount=analysis_result.get('total_identified_loss', 0),
                leakage_percentage=analysis_result['financial_summary'].get('loss_percentage', 0),
                risk_score=0,
                user_id=current_user.id
            )
            db.add(db_analysis)
            db.commit()
        except Exception as db_error:
            print(f"Database save error (non-critical): {db_error}")
        
        # Return response
        return {
            "success": True,
            "analysis": analysis_result
        }
        
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@router.get("/analysis/{analysis_id}")
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
    
    return {
        "success": True,
        "analysis": {
            "analysis_id": analysis.analysis_id,
            "business_name": analysis.business_name,
            "business_stage": analysis.business_stage,
            "created_at": analysis.created_at,
            "leakage_points": analysis.leakage_points,
            "total_revenue": analysis.total_revenue,
            "leakage_amount": analysis.leakage_amount,
            "leakage_percentage": analysis.leakage_percentage
        }
    }

@router.get("/history")
async def get_analysis_history(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List all business analyses with pagination
    """
    analyses = db.query(BusinessAnalysis).order_by(
        BusinessAnalysis.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "analyses": [
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
    }

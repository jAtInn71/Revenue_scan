"""
AI Insights API routes - Chat with AI for revenue analysis
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json

from database.database import get_db, User, BusinessAnalysis, UploadedData
from services.auth_service import get_current_user
from services.ai_service import AIService
from core.config import settings

router = APIRouter()

class Message(BaseModel):
    role: str  # user or assistant
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None

@router.post("/")
async def get_ai_insight(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered insights and recommendations
    """
    
    # Get user's business context
    recent_analyses = db.query(BusinessAnalysis).filter(
        BusinessAnalysis.business_name == current_user.company_name
    ).order_by(BusinessAnalysis.created_at.desc()).limit(3).all()
    
    recent_uploads = db.query(UploadedData).filter(
        UploadedData.user_id == current_user.id
    ).order_by(UploadedData.created_at.desc()).limit(2).all()
    
    # Build context for AI
    context = {
        "user": {
            "company": current_user.company_name,
            "role": current_user.role
        },
        "recent_analyses": [
            {
                "business_model": analysis.business_model,
                "total_revenue": analysis.total_revenue,
                "leakage_amount": analysis.leakage_amount,
                "risk_score": analysis.risk_score
            }
            for analysis in recent_analyses
        ] if recent_analyses else [],
        "recent_uploads": [
            {
                "file_name": upload.file_name,
                "total_rows": upload.total_rows,
                "leakages_detected": len(upload.leakage_data.get("items", [])) if upload.leakage_data else 0
            }
            for upload in recent_uploads
        ] if recent_uploads else []
    }
    
    # Get AI response
    ai_service = AIService()
    
    try:
        response = await ai_service.generate_chat_response(
            user_message=request.message,
            context=context
        )
        
        return {
            "response": response["content"],
            "keyDrivers": response.get("key_drivers", []),
            "suggestedActions": response.get("suggested_actions", []),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        # Fallback to rule-based response
        return _generate_fallback_response(request.message, context)

@router.post("/explain/{upload_id}")
async def explain_leakage(
    upload_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI explanation for specific leakage detection
    """
    
    upload = db.query(UploadedData).filter(
        UploadedData.upload_id == upload_id,
        UploadedData.user_id == current_user.id
    ).first()
    
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    ai_service = AIService()
    
    try:
        explanation = await ai_service.explain_leakage_data(
            leakage_data=upload.leakage_data,
            business_context={
                "company": current_user.company_name,
                "file_name": upload.file_name
            }
        )
        
        return {
            "explanation": explanation["content"],
            "recommendations": explanation.get("recommendations", []),
            "severity_analysis": explanation.get("severity_analysis", {})
        }
        
    except Exception as e:
        return {
            "explanation": f"Analysis of {upload.file_name} shows {len(upload.leakage_data.get('items', []))} potential revenue leakage points.",
            "recommendations": [
                "Review highlighted transactions for accuracy",
                "Implement automated validation checks",
                "Set up alerts for similar patterns"
            ]
        }

def _generate_fallback_response(message: str, context: dict) -> dict:
    """
    Generate rule-based response when AI is unavailable
    """
    
    message_lower = message.lower()
    
    # Question matching
    if any(word in message_lower for word in ['reduce', 'prevent', 'stop', 'leakage']):
        return {
            "response": "To reduce revenue leakage, I recommend:\n\n1. **Automate Invoice Verification**: Implement automated checks to catch pricing errors before invoices are sent.\n\n2. **Regular Reconciliation**: Schedule weekly revenue reconciliation to catch discrepancies early.\n\n3. **Customer Contract Reviews**: Audit active contracts quarterly to ensure proper billing.\n\n4. **Payment Failure Alerts**: Set up real-time notifications for failed payments to enable immediate follow-up.",
            "keyDrivers": [
                "Automation reduces human error",
                "Early detection minimizes losses",
                "Proactive monitoring prevents issues"
            ],
            "suggestedActions": [
                "Set up automated billing verification",
                "Create weekly reconciliation schedule",
                "Review top 20% of customer contracts",
                "Enable payment failure alerts"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    elif any(word in message_lower for word in ['dashboard', 'metrics', 'kpi']):
        total_revenue = sum(a["total_revenue"] for a in context["recent_analyses"])
        total_leakage = sum(a["leakage_amount"] for a in context["recent_analyses"])
        
        return {
            "response": f"Based on your recent data:\n\n**Revenue Overview:**\n- Total Revenue Analyzed: ${total_revenue:,.2f}\n- Revenue Leakage Detected: ${total_leakage:,.2f}\n- Leakage Rate: {(total_leakage/total_revenue*100) if total_revenue > 0 else 0:.1f}%\n\n**Key Insights:**\n- Your leakage rate is {'above' if (total_leakage/total_revenue*100) > 5 else 'below'} industry average (5%)\n- Focus on your top revenue streams first for maximum impact\n- Regular monitoring will help catch issues early",
            "keyDrivers": [
                "Data-driven decision making",
                "Focus on high-impact areas",
                "Continuous improvement"
            ],
            "suggestedActions": [
                "Review top 3 revenue categories",
                "Set monthly review cadence",
                "Track improvement over time"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    else:
        return {
            "response": "I'm here to help you identify and prevent revenue leakage! I can assist with:\n\n• **Analyzing your data** for hidden revenue losses\n• **Identifying patterns** in pricing errors, unbilled services, and payment failures\n• **Recommending strategies** to recover and prevent future leakage\n• **Explaining insights** from your uploaded data\n\nWhat specific area would you like to explore?",
            "keyDrivers": [
                "Comprehensive revenue analysis",
                "Pattern recognition",
                "Actionable recommendations"
            ],
            "suggestedActions": [
                "Upload your transaction data",
                "Ask about specific leakage types",
                "Review your dashboard metrics"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }

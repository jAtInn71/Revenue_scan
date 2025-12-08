"""
AI Chatbot API Routes
Business consultant chatbot for revenue optimization and business advice
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database.database import get_db, User, BusinessAnalysis, UploadedData
from services.auth_service import get_current_user
from services.chatbot_service import BusinessChatbot, ConversationManager

router = APIRouter()
chatbot = BusinessChatbot()
conversation_manager = ConversationManager()


class ChatMessage(BaseModel):
    message: str
    clear_history: Optional[bool] = False


class ChatResponse(BaseModel):
    answer: str
    topic: str
    suggestions: List[str]
    resources: List[dict]
    timestamp: str


@router.post("/", response_model=ChatResponse)
async def chat_with_ai(
    chat_message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with AI business consultant
    Provides intelligent advice on revenue optimization, cost reduction, and business strategy
    """
    
    # Clear history if requested
    if chat_message.clear_history:
        conversation_manager.clear_history(str(current_user.id))
    
    # Get conversation history
    history = conversation_manager.get_history(str(current_user.id))
    
    # Build context from user data
    context = {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "company": getattr(current_user, 'company', None)
        }
    }
    
    # Get recent analyses for context (no user_id filter for now)
    recent_analyses = db.query(BusinessAnalysis).order_by(
        BusinessAnalysis.created_at.desc()
    ).limit(3).all()
    
    if recent_analyses:
        context["recent_analyses"] = [
            {
                "total_revenue": a.total_revenue if hasattr(a, 'total_revenue') else 0,
                "leakage_amount": a.leakage_amount if hasattr(a, 'leakage_amount') else 0
            }
            for a in recent_analyses
        ]
    
    # Get latest upload for context
    latest_upload = db.query(UploadedData).filter(
        UploadedData.user_id == current_user.id
    ).order_by(UploadedData.created_at.desc()).first()
    
    if latest_upload:
        context["latest_upload"] = {
            "file_name": latest_upload.file_name,
            "total_rows": latest_upload.total_rows,
            "leakages_detected": len(latest_upload.leakage_data.get("items", [])) if latest_upload.leakage_data else 0
        }
    
    # Get AI response
    response = await chatbot.chat(
        message=chat_message.message,
        context=context,
        conversation_history=history
    )
    
    # Save to conversation history
    conversation_manager.add_message(str(current_user.id), "user", chat_message.message)
    conversation_manager.add_message(str(current_user.id), "assistant", response["answer"])
    
    return ChatResponse(**response)


@router.get("/history")
async def get_chat_history(
    current_user: User = Depends(get_current_user)
):
    """Get conversation history for current user"""
    history = conversation_manager.get_history(str(current_user.id))
    
    return {
        "history": history,
        "message_count": len(history)
    }


@router.delete("/history")
async def clear_chat_history(
    current_user: User = Depends(get_current_user)
):
    """Clear conversation history for current user"""
    conversation_manager.clear_history(str(current_user.id))
    
    return {
        "message": "Chat history cleared successfully"
    }


@router.get("/suggestions")
async def get_chat_suggestions(
    topic: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get contextual chat suggestions based on user's data
    """
    suggestions = []
    
    # Get user's latest data for contextual suggestions
    latest_analysis = db.query(BusinessAnalysis).filter(
        BusinessAnalysis.user_id == current_user.id
    ).order_by(BusinessAnalysis.created_at.desc()).first()
    
    latest_upload = db.query(UploadedData).filter(
        UploadedData.user_id == current_user.id
    ).order_by(UploadedData.created_at.desc()).first()
    
    if latest_analysis:
        if latest_analysis.leakage_percentage > 10:
            suggestions.append({
                "question": "How can I reduce my revenue leakage?",
                "priority": "high"
            })
        
        if latest_analysis.risk_score > 70:
            suggestions.append({
                "question": "What are the biggest risks to my revenue?",
                "priority": "high"
            })
        
        if latest_analysis.total_revenue > 0:
            suggestions.append({
                "question": "How can I increase my revenue by 20%?",
                "priority": "medium"
            })
    
    if latest_upload and latest_upload.leakage_data:
        leakage_count = len(latest_upload.leakage_data.get("items", []))
        if leakage_count > 5:
            suggestions.append({
                "question": f"I have {leakage_count} issues detected. Which should I fix first?",
                "priority": "high"
            })
    
    # Add general suggestions if none specific
    if not suggestions:
        suggestions = [
            {"question": "How can I improve my business profitability?", "priority": "medium"},
            {"question": "What metrics should I track for my business?", "priority": "medium"},
            {"question": "How do I reduce costs without hurting quality?", "priority": "medium"},
            {"question": "What's the best pricing strategy for my business?", "priority": "low"}
        ]
    
    return {
        "suggestions": suggestions,
        "personalized": bool(latest_analysis or latest_upload)
    }


@router.get("/topics")
async def get_chat_topics():
    """Get available chat topics and example questions"""
    
    topics = {
        "Revenue Growth": [
            "How can I increase my revenue?",
            "What are quick wins to boost sales?",
            "How do I identify underpriced products?"
        ],
        "Cost Reduction": [
            "Where should I look for cost savings?",
            "How can I reduce operational expenses?",
            "What costs have the highest ROI when reduced?"
        ],
        "Pricing Strategy": [
            "How do I set optimal prices?",
            "When should I offer discounts?",
            "What's a healthy discount percentage?"
        ],
        "Revenue Leakage": [
            "What causes revenue leakage?",
            "How can I prevent revenue loss?",
            "How do I audit for revenue leaks?"
        ],
        "Customer Management": [
            "How do I improve customer retention?",
            "How can I reduce customer churn?",
            "What's a good customer lifetime value?"
        ],
        "Data & Analytics": [
            "What metrics should I track daily?",
            "How do I analyze my revenue data?",
            "What KPIs matter most?"
        ]
    }
    
    return {
        "topics": topics,
        "total_topics": len(topics)
    }

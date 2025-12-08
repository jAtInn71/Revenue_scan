"""
Dashboard API routes - Metrics, Charts, Analytics
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random

from database.database import (
    get_db, User, BusinessAnalysis, UploadedData, 
    Alert, Notification
)
from services.auth_service import get_current_user

router = APIRouter()

@router.get("/")
async def get_dashboard_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive dashboard data including metrics, charts, and recent activity
    Uses REAL data from uploaded files
    """
    
    # Get all uploads for current user
    uploads = db.query(UploadedData).filter(
        UploadedData.user_id == current_user.id,
        UploadedData.status == "completed"
    ).order_by(UploadedData.created_at.desc()).all()
    
    # Calculate real metrics from uploads
    total_revenue = 0
    total_costs = 0
    total_leakage = 0
    total_rows = 0
    leakage_by_category = {}
    leakage_by_severity = {"high": 0, "medium": 0, "low": 0}
    revenue_by_month = {}
    
    for upload in uploads:
        # Get leakage data
        if upload.leakage_data:
            leakage_items = upload.leakage_data.get("items", [])
            upload_leakage = upload.leakage_data.get("total_amount", 0)
            total_leakage += upload_leakage
            
            # Categorize leakages
            for item in leakage_items:
                category = item.get("category", "Other")
                severity = item.get("severity", "low")
                amount = item.get("amount", 0)
                
                leakage_by_category[category] = leakage_by_category.get(category, 0) + amount
                leakage_by_severity[severity] = leakage_by_severity.get(severity, 0) + 1
        
        # Get data summary for revenue/costs
        if upload.data_summary:
            column_details = upload.data_summary.get("column_details", {})
            
            for col_name, details in column_details.items():
                col_sum = details.get("sum", 0)
                if col_sum:
                    col_lower = col_name.lower()
                    # Revenue columns
                    if any(term in col_lower for term in ['revenue', 'sales', 'income', 'amount', 'total', 'price']):
                        total_revenue += col_sum
                    # Cost columns
                    elif any(term in col_lower for term in ['cost', 'expense', 'cogs', 'spend']):
                        total_costs += col_sum
            
            total_rows += upload.total_rows or 0
            
            # Group by month
            month_key = upload.created_at.strftime("%b %Y")
            if month_key not in revenue_by_month:
                revenue_by_month[month_key] = {"revenue": 0, "leakage": 0, "uploads": 0}
            
            revenue_by_month[month_key]["uploads"] += 1
            revenue_by_month[month_key]["leakage"] += upload.leakage_data.get("total_amount", 0) if upload.leakage_data else 0
    
    # Calculate metrics
    net_profit = total_revenue - total_costs
    profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
    leakage_percentage = (total_leakage / total_revenue * 100) if total_revenue > 0 else 0
    
    # Risk score based on leakage percentage
    if leakage_percentage > 20:
        risk_score = 85
        risk_level = "Critical"
    elif leakage_percentage > 10:
        risk_score = 65
        risk_level = "High"
    elif leakage_percentage > 5:
        risk_score = 45
        risk_level = "Medium"
    else:
        risk_score = 25
        risk_level = "Low"
    
    # Get recent alerts
    recent_alerts = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    # Chart data - Revenue vs Leakage by month
    revenue_chart = []
    for month, data_dict in sorted(revenue_by_month.items(), key=lambda x: datetime.strptime(x[0], "%b %Y")):
        revenue_chart.append({
            "month": month,
            "revenue": round(data_dict["revenue"], 2),
            "leakage": round(data_dict["leakage"], 2)
        })
    
    # If no data, show last 6 months with zeros
    if not revenue_chart:
        for i in range(6):
            month_date = datetime.now() - timedelta(days=30 * (5 - i))
            revenue_chart.append({
                "month": month_date.strftime("%b %Y"),
                "revenue": 0,
                "leakage": 0
            })
    
    # Leakage by Category chart
    category_chart = [
        {"name": category, "value": round(amount, 2)}
        for category, amount in leakage_by_category.items()
    ]
    
    # Leakage by Severity
    severity_chart = [
        {"name": "Critical", "value": leakage_by_severity.get("high", 0), "color": "#ef4444"},
        {"name": "Warning", "value": leakage_by_severity.get("medium", 0), "color": "#f59e0b"},
        {"name": "Info", "value": leakage_by_severity.get("low", 0), "color": "#3b82f6"}
    ]
    
    # Generate AI insight based on real data
    ai_insight = _generate_ai_insight(
        total_revenue, total_leakage, leakage_percentage, 
        leakage_by_category, len(uploads)
    )
    
    return {
        "metrics": {
            "totalRevenue": round(total_revenue, 2),
            "totalRevenueChange": 0,  # Could calculate vs previous period
            "totalCosts": round(total_costs, 2),
            "netProfit": round(net_profit, 2),
            "profitMargin": round(profit_margin, 2),
            "leakageDetected": round(total_leakage, 2),
            "leakagePercentage": round(leakage_percentage, 2),
            "leakageDetectedChange": 0,
            "riskScore": risk_score,
            "riskLevel": risk_level,
            "riskScoreChange": 0,
            "analysesRun": len(uploads),
            "totalTransactions": total_rows,
            "analysesRunChange": 0
        },
        "charts": {
            "revenueVsLeakage": revenue_chart[-6:],  # Last 6 months
            "leakageByCategory": category_chart,
            "leakageBySegment": severity_chart
        },
        "recentAlerts": [
            {
                "id": alert.notification_id,
                "title": alert.title,
                "message": alert.message,
                "severity": alert.severity,
                "timestamp": alert.created_at.isoformat(),
                "isRead": alert.is_read
            }
            for alert in recent_alerts
        ],
        "aiInsight": ai_insight
    }

def _generate_ai_insight(revenue, leakage, leakage_pct, categories, upload_count):
    """Generate AI insight based on real data"""
    if upload_count == 0:
        return {
            "title": "Welcome to Revenue Advisor",
            "message": "Upload your first dataset to get AI-powered insights and revenue leakage analysis."
        }
    
    if leakage_pct > 20:
        return {
            "title": "🚨 Critical Revenue Leakage Detected",
            "message": f"Your data shows {leakage_pct:.1f}% revenue leakage (${leakage:,.2f}). Immediate action required! Focus on: {', '.join(list(categories.keys())[:3])}. Implementing fixes could recover ${leakage * 0.7:,.2f}."
        }
    elif leakage_pct > 10:
        return {
            "title": "⚠️ Significant Revenue Opportunity",
            "message": f"Detected {leakage_pct:.1f}% revenue leakage (${leakage:,.2f}). Top issue: {list(categories.keys())[0] if categories else 'Data Quality'}. Quick wins available - estimated recovery: ${leakage * 0.5:,.2f}."
        }
    elif leakage_pct > 5:
        return {
            "title": "📊 Revenue Optimization Available",
            "message": f"Found {leakage_pct:.1f}% revenue leakage (${leakage:,.2f}). Focus on process improvements in {list(categories.keys())[0] if categories else 'operations'} to recover ${leakage * 0.3:,.2f}."
        }
    else:
        return {
            "title": "✅ Revenue Health Looking Good",
            "message": f"Only {leakage_pct:.1f}% leakage detected across ${revenue:,.2f} in revenue. Continue monitoring and maintain current best practices. {upload_count} analyses completed."
        }

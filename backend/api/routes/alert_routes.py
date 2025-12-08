"""
Alert Management API routes - Create, update, delete alerts
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

from database.database import get_db, User, Alert, Notification
from services.auth_service import get_current_user
from services.alert_service import AVAILABLE_METRICS, get_metric_description, get_alert_summary

router = APIRouter()

class AlertCreate(BaseModel):
    name: str
    description: Optional[str] = None
    metric: str
    condition: str
    threshold: float
    severity: str
    notify_email: bool = True
    notify_in_app: bool = True

class AlertUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    threshold: Optional[float] = None
    severity: Optional[str] = None
    is_active: Optional[bool] = None

@router.get("/")
async def get_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all alerts for current user
    """
    alerts = db.query(Alert).filter(
        Alert.user_id == current_user.id
    ).order_by(Alert.created_at.desc()).all()
    
    return [
        {
            "id": alert.alert_id,
            "name": alert.name,
            "description": alert.description,
            "metric": alert.metric,
            "condition": alert.condition,
            "threshold": alert.threshold,
            "severity": alert.severity,
            "notifyEmail": alert.notify_email,
            "notifyInApp": alert.notify_in_app,
            "isActive": alert.is_active,
            "createdAt": alert.created_at.isoformat(),
            "updatedAt": alert.updated_at.isoformat()
        }
        for alert in alerts
    ]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_data: AlertCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new alert
    """
    alert_id = f"ALERT-{str(uuid.uuid4())[:8]}"
    
    new_alert = Alert(
        alert_id=alert_id,
        user_id=current_user.id,
        name=alert_data.name,
        description=alert_data.description,
        metric=alert_data.metric,
        condition=alert_data.condition,
        threshold=alert_data.threshold,
        severity=alert_data.severity,
        notify_email=alert_data.notify_email,
        notify_in_app=alert_data.notify_in_app,
        is_active=True
    )
    
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    
    return {
        "id": new_alert.alert_id,
        "name": new_alert.name,
        "message": "Alert created successfully"
    }

@router.put("/{alert_id}")
async def update_alert(
    alert_id: str,
    alert_data: AlertUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing alert
    """
    alert = db.query(Alert).filter(
        Alert.alert_id == alert_id,
        Alert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Update fields
    if alert_data.name is not None:
        alert.name = alert_data.name
    if alert_data.description is not None:
        alert.description = alert_data.description
    if alert_data.threshold is not None:
        alert.threshold = alert_data.threshold
    if alert_data.severity is not None:
        alert.severity = alert_data.severity
    if alert_data.is_active is not None:
        alert.is_active = alert_data.is_active
    
    alert.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(alert)
    
    return {
        "id": alert.alert_id,
        "message": "Alert updated successfully"
    }

@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an alert
    """
    alert = db.query(Alert).filter(
        Alert.alert_id == alert_id,
        Alert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db.delete(alert)
    db.commit()
    
    return None

@router.patch("/{alert_id}/status")
async def toggle_alert_status(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle alert active/inactive status
    """
    alert = db.query(Alert).filter(
        Alert.alert_id == alert_id,
        Alert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_active = not alert.is_active
    alert.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(alert)
    
    return {
        "id": alert.alert_id,
        "isActive": alert.is_active,
        "message": f"Alert {'activated' if alert.is_active else 'deactivated'}"
    }


@router.get("/metrics/")
async def get_available_metrics(
    current_user: User = Depends(get_current_user)
):
    """
    Get list of available metrics that can be monitored with alerts
    """
    return {
        "metrics": AVAILABLE_METRICS,
        "conditions": [
            {"value": "greater_than", "label": "Greater Than (>)"},
            {"value": "less_than", "label": "Less Than (<)"},
            {"value": "equals", "label": "Equals (=)"},
            {"value": "not_equals", "label": "Not Equals (≠)"}
        ],
        "severities": [
            {"value": "critical", "label": "Critical", "color": "red"},
            {"value": "high", "label": "High", "color": "orange"},
            {"value": "medium", "label": "Medium", "color": "yellow"},
            {"value": "low", "label": "Low", "color": "green"}
        ]
    }


@router.get("/summary/")
async def get_alert_summary_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get summary statistics about user's alerts
    """
    return get_alert_summary(db, current_user.id)

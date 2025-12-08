"""
Alert Evaluation Service
Automatically evaluates alerts based on uploaded data analysis
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from database.database import Alert, Notification, UploadedData
from datetime import datetime
import json


def calculate_metric_value(
    metric: str,
    upload_data: UploadedData,
    leakage_data: List[Dict],
    data_summary: Dict
) -> float:
    """
    Calculate the current value for a specific metric based on upload data
    
    Supported Metrics:
    - revenue_total: Total revenue from all revenue columns
    - high_leakage: Total amount of revenue leakage detected
    - leakage_percentage: Leakage as % of revenue
    - negative_revenue: Count of negative revenue transactions
    - missing_data: Percentage of missing data
    - duplicate_transactions: Count of duplicate records
    - data_quality_score: Overall data quality score (0-100)
    - excessive_costs: Count of excessive cost entries
    - profit_margin: Profit margin percentage
    - zero_revenue: Count of zero revenue transactions
    """
    
    try:
        # Parse JSON fields if they're strings
        if isinstance(leakage_data, str):
            leakage_data = json.loads(leakage_data) if leakage_data else []
        if isinstance(data_summary, str):
            data_summary = json.loads(data_summary) if data_summary else {}
        
        financial_summary = data_summary.get('financial_summary', {})
        ai_analysis = data_summary.get('ai_analysis', {})
        
        # Calculate based on metric type
        if metric == "revenue_total":
            return financial_summary.get('total_revenue', 0)
        
        elif metric == "high_leakage":
            # Sum all leakage amounts
            total_leakage = 0
            for leakage in leakage_data:
                if 'amount' in leakage:
                    total_leakage += abs(leakage['amount'])
            return total_leakage
        
        elif metric == "leakage_percentage":
            total_revenue = financial_summary.get('total_revenue', 1)
            total_leakage = 0
            for leakage in leakage_data:
                if 'amount' in leakage:
                    total_leakage += abs(leakage['amount'])
            return (total_leakage / total_revenue * 100) if total_revenue > 0 else 0
        
        elif metric == "negative_revenue":
            count = 0
            for leakage in leakage_data:
                if leakage.get('type') == 'Negative Revenue Values':
                    count += leakage.get('affected_rows', 0)
            return count
        
        elif metric == "zero_revenue":
            count = 0
            for leakage in leakage_data:
                if leakage.get('type') == 'Zero Revenue Transactions':
                    count += leakage.get('affected_rows', 0)
            return count
        
        elif metric == "missing_data":
            # Calculate % of missing data across all columns
            column_details = data_summary.get('column_details', {})
            total_nulls = 0
            total_rows = upload_data.total_rows or 1
            num_columns = len(column_details)
            
            for col_name, col_info in column_details.items():
                total_nulls += col_info.get('null_count', 0)
            
            total_cells = total_rows * num_columns if num_columns > 0 else 1
            return (total_nulls / total_cells * 100) if total_cells > 0 else 0
        
        elif metric == "duplicate_transactions":
            count = 0
            for leakage in leakage_data:
                if leakage.get('type') == 'Duplicate Transactions':
                    count += leakage.get('affected_rows', 0)
            return count
        
        elif metric == "data_quality_score":
            # Calculate quality score: 100 - (error percentage)
            total_issues = len(leakage_data)
            total_rows = upload_data.total_rows or 1
            error_percentage = (total_issues / total_rows * 100) if total_rows > 0 else 0
            return max(0, 100 - error_percentage)
        
        elif metric == "excessive_costs":
            count = 0
            for leakage in leakage_data:
                if leakage.get('type') == 'Excessive Costs':
                    count += leakage.get('affected_rows', 0)
            return count
        
        elif metric == "profit_margin":
            return financial_summary.get('profit_margin', 0)
        
        elif metric == "total_costs":
            return financial_summary.get('total_costs', 0)
        
        elif metric == "net_profit":
            return financial_summary.get('net_profit', 0)
        
        else:
            # Unknown metric
            return 0
            
    except Exception as e:
        print(f"Error calculating metric {metric}: {e}")
        return 0


def check_condition(current_value: float, condition: str, threshold: float) -> bool:
    """
    Check if the condition is met
    """
    if condition == "greater_than":
        return current_value > threshold
    elif condition == "less_than":
        return current_value < threshold
    elif condition == "equals":
        return abs(current_value - threshold) < 0.01  # Allow small float difference
    elif condition == "not_equals":
        return abs(current_value - threshold) >= 0.01
    else:
        return False


def format_metric_value(metric: str, value: float) -> str:
    """
    Format the metric value for display in notifications
    """
    if metric in ["revenue_total", "high_leakage", "total_costs", "net_profit"]:
        return f"${value:,.2f}"
    elif metric in ["leakage_percentage", "missing_data", "data_quality_score", "profit_margin"]:
        return f"{value:.1f}%"
    else:
        return f"{int(value)}"


def evaluate_alerts_on_upload(
    db: Session,
    user_id: str,
    upload_data: UploadedData
) -> List[Dict[str, Any]]:
    """
    Evaluate all active alerts for a user based on uploaded data
    Returns list of triggered alerts with notification info
    """
    triggered_alerts = []
    
    try:
        # Get all active alerts for the user
        active_alerts = db.query(Alert).filter(
            Alert.user_id == user_id,
            Alert.is_active == True
        ).all()
        
        if not active_alerts:
            return triggered_alerts
        
        # Parse upload data
        leakage_data = upload_data.leakage_data
        data_summary = upload_data.data_summary
        
        # Evaluate each alert
        for alert in active_alerts:
            try:
                # Calculate current metric value
                current_value = calculate_metric_value(
                    metric=alert.metric,
                    upload_data=upload_data,
                    leakage_data=leakage_data,
                    data_summary=data_summary
                )
                
                # Check if condition is met
                if check_condition(current_value, alert.condition, alert.threshold):
                    # Alert TRIGGERED!
                    formatted_value = format_metric_value(alert.metric, current_value)
                    formatted_threshold = format_metric_value(alert.metric, alert.threshold)
                    
                    # Create notification message
                    message = (
                        f"Alert '{alert.name}' triggered!\n"
                        f"Current value: {formatted_value}\n"
                        f"Threshold: {alert.condition.replace('_', ' ')} {formatted_threshold}\n"
                        f"File: {upload_data.file_name}"
                    )
                    
                    # Create in-app notification if enabled
                    if alert.notify_in_app:
                        notification = Notification(
                            user_id=user_id,
                            title=f"{alert.severity.upper()}: {alert.name}",
                            message=message,
                            severity=alert.severity,
                            related_type="alert",
                            related_id=alert.alert_id,
                            is_read=False,
                            created_at=datetime.utcnow()
                        )
                        db.add(notification)
                    
                    # Store triggered alert info
                    triggered_alerts.append({
                        "alert_id": alert.alert_id,
                        "alert_name": alert.name,
                        "metric": alert.metric,
                        "current_value": current_value,
                        "formatted_value": formatted_value,
                        "threshold": alert.threshold,
                        "condition": alert.condition,
                        "severity": alert.severity,
                        "notify_email": alert.notify_email,
                        "message": message
                    })
                    
            except Exception as e:
                print(f"Error evaluating alert {alert.alert_id}: {e}")
                continue
        
        # Commit all notifications
        if triggered_alerts:
            db.commit()
        
        return triggered_alerts
        
    except Exception as e:
        print(f"Error in evaluate_alerts_on_upload: {e}")
        db.rollback()
        return []


def get_alert_summary(db: Session, user_id: str) -> Dict[str, Any]:
    """
    Get summary of alerts for a user
    """
    total_alerts = db.query(Alert).filter(Alert.user_id == user_id).count()
    active_alerts = db.query(Alert).filter(
        Alert.user_id == user_id,
        Alert.is_active == True
    ).count()
    
    critical_alerts = db.query(Alert).filter(
        Alert.user_id == user_id,
        Alert.severity == "critical",
        Alert.is_active == True
    ).count()
    
    return {
        "total_alerts": total_alerts,
        "active_alerts": active_alerts,
        "critical_alerts": critical_alerts
    }


def get_metric_description(metric: str) -> str:
    """
    Get human-readable description of metric
    """
    descriptions = {
        "revenue_total": "Total revenue from all revenue columns",
        "high_leakage": "Total amount of revenue leakage detected",
        "leakage_percentage": "Revenue leakage as percentage of total revenue",
        "negative_revenue": "Number of negative revenue transactions",
        "zero_revenue": "Number of zero revenue transactions",
        "missing_data": "Percentage of missing data across all columns",
        "duplicate_transactions": "Number of duplicate transaction records",
        "data_quality_score": "Overall data quality score (0-100)",
        "excessive_costs": "Number of excessive cost entries detected",
        "profit_margin": "Profit margin percentage",
        "total_costs": "Total costs from all cost columns",
        "net_profit": "Net profit (revenue minus costs)"
    }
    return descriptions.get(metric, "Unknown metric")


# List of all available metrics for UI
AVAILABLE_METRICS = [
    {"value": "revenue_total", "label": "Total Revenue", "unit": "currency"},
    {"value": "high_leakage", "label": "Revenue Leakage", "unit": "currency"},
    {"value": "leakage_percentage", "label": "Leakage Percentage", "unit": "percentage"},
    {"value": "negative_revenue", "label": "Negative Revenue Count", "unit": "count"},
    {"value": "zero_revenue", "label": "Zero Revenue Count", "unit": "count"},
    {"value": "missing_data", "label": "Missing Data Percentage", "unit": "percentage"},
    {"value": "duplicate_transactions", "label": "Duplicate Transactions", "unit": "count"},
    {"value": "data_quality_score", "label": "Data Quality Score", "unit": "percentage"},
    {"value": "excessive_costs", "label": "Excessive Costs Count", "unit": "count"},
    {"value": "profit_margin", "label": "Profit Margin", "unit": "percentage"},
    {"value": "total_costs", "label": "Total Costs", "unit": "currency"},
    {"value": "net_profit", "label": "Net Profit", "unit": "currency"},
]

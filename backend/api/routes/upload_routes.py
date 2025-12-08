"""
Data Upload API routes - CSV/Excel file upload and processing
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
import pandas as pd
import uuid
import os
import json
from typing import Optional

from database.database import get_db, User, UploadedData
from services.auth_service import get_current_user
from services.ai_service import AIService
from services.alert_service import evaluate_alerts_on_upload
from core.config import settings

router = APIRouter()
ai_service = AIService()

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    column_mapping: Optional[str] = Form(None),
    sheet_name: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload CSV or Excel file for revenue leakage analysis
    sheet_name: Optional - specify which Excel sheet to read (default: first sheet)
    """
    
    # Validate file type
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_extension} not allowed. Allowed types: {settings.ALLOWED_FILE_TYPES}"
        )
    
    # Validate file size
    file_content = await file.read()
    if len(file_content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE / (1024*1024)}MB"
        )
    
    # Generate upload ID
    upload_id = f"UPLOAD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
    
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, f"{upload_id}{file_extension}")
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # Parse file
    try:
        sheet_names = None
        selected_sheet = None
        
        if file_extension == ".csv":
            df = pd.read_csv(file_path)
        else:  # Excel - handle multiple sheets
            # Get all sheet names
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            
            # Determine which sheet to read
            if sheet_name and sheet_name in sheet_names:
                selected_sheet = sheet_name
            else:
                selected_sheet = sheet_names[0]  # Default to first sheet
            
            # Read the selected sheet
            df = pd.read_excel(file_path, sheet_name=selected_sheet)
        
        # Get data statistics
        total_rows = len(df)
        total_columns = len(df.columns)
        
        # Generate COMPREHENSIVE data summary for ALL columns
        column_details = {}
        for col in df.columns:
            col_data = {
                "name": col,
                "data_type": str(df[col].dtype),
                "null_count": int(df[col].isnull().sum()),
                "null_percentage": float((df[col].isnull().sum() / total_rows * 100)) if total_rows > 0 else 0,
                "unique_values": int(df[col].nunique()),
            }
            
            # Add numeric statistics if column is numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                col_data.update({
                    "min": float(df[col].min()) if not df[col].isna().all() else None,
                    "max": float(df[col].max()) if not df[col].isna().all() else None,
                    "mean": float(df[col].mean()) if not df[col].isna().all() else None,
                    "median": float(df[col].median()) if not df[col].isna().all() else None,
                    "sum": float(df[col].sum()) if not df[col].isna().all() else None,
                    "std": float(df[col].std()) if not df[col].isna().all() else None,
                    "negative_count": int((df[col] < 0).sum()),
                    "zero_count": int((df[col] == 0).sum()),
                })
            else:
                # For text columns, add top values
                top_values = df[col].value_counts().head(5).to_dict()
                col_data["top_values"] = {str(k): int(v) for k, v in top_values.items()}
            
            column_details[col] = col_data
        
        # Generate data summary with FULL column information
        data_summary = {
            "total_rows": total_rows,
            "total_columns": total_columns,
            "columns": list(df.columns),
            "column_details": column_details,
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "nulls": {col: int(df[col].isnull().sum()) for col in df.columns},
            "sample_data": df.head(10).to_dict('records'),  # Show 10 sample rows
            "memory_usage": int(df.memory_usage(deep=True).sum()),
            "sheet_names": sheet_names,  # List of all sheets (Excel only)
            "selected_sheet": selected_sheet,  # Which sheet was analyzed
        }
        
        # Parse column mapping if provided
        mapping = json.loads(column_mapping) if column_mapping else {}
        
        # Detect potential leakages
        leakage_data = _analyze_data_for_leakages(df, mapping)
        
        # Get comprehensive AI analysis of full dataset
        ai_analysis_result = await ai_service.analyze_full_dataset(df, file.filename, leakage_data)
        
        # Create database record
        upload_record = UploadedData(
            upload_id=upload_id,
            user_id=current_user.id,
            file_name=file.filename,
            file_path=file_path,
            file_size=len(file_content),
            file_type=file_extension,
            column_mapping=mapping,
            total_rows=total_rows,
            total_columns=total_columns,
            data_summary=data_summary,
            leakage_data=leakage_data,
            status="completed"
        )
        
        db.add(upload_record)
        db.commit()
        db.refresh(upload_record)
        
        # Prepare leakage summary
        leakage_summary = {
            "total_leakages": leakage_data["total_leakages"],
            "total_amount": leakage_data["total_amount"],
            "critical": len([l for l in leakage_data["items"] if l["severity"] == "high"]),
            "warnings": len([l for l in leakage_data["items"] if l["severity"] in ["medium", "low"]]),
            "top_issues": leakage_data["items"][:5]  # Top 5 leakages
        }
        
        # 🚨 EVALUATE ALERTS - Check if any alerts should be triggered
        triggered_alerts = evaluate_alerts_on_upload(
            db=db,
            user_id=current_user.id,
            upload_data=upload_record
        )
        
        return {
            "upload_id": upload_id,
            "file_name": file.filename,
            "rows_count": total_rows,
            "total_rows": total_rows,
            "total_columns": total_columns,
            "status": "completed",
            "summary": data_summary,
            "sheet_names": sheet_names,  # All available sheets (Excel)
            "selected_sheet": selected_sheet,  # Currently analyzed sheet
            "leakages_detected": len(leakage_data["items"]),
            "leakage_summary": leakage_summary,
            "ai_analysis": ai_analysis_result,
            "financial_summary": ai_analysis_result.get("financial_summary", {}),
            "kpis": ai_analysis_result.get("kpis", {}),
            "alerts_triggered": len(triggered_alerts),
            "triggered_alerts": triggered_alerts  # List of alerts that were triggered
        }
        
    except Exception as e:
        # Update status to failed
        upload_record = UploadedData(
            upload_id=upload_id,
            user_id=current_user.id,
            file_name=file.filename,
            file_path=file_path,
            file_size=len(file_content),
            file_type=file_extension,
            status="failed",
            error_message=str(e)
        )
        db.add(upload_record)
        db.commit()
        
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process file: {str(e)}"
        )

@router.get("/history")
async def get_upload_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get upload history for current user
    """
    uploads = db.query(UploadedData).filter(
        UploadedData.user_id == current_user.id
    ).order_by(UploadedData.created_at.desc()).all()
    
    return [
        {
            "upload_id": upload.upload_id,
            "file_name": upload.file_name,
            "file_size": upload.file_size,
            "total_rows": upload.total_rows,
            "status": upload.status,
            "created_at": upload.created_at.isoformat()
        }
        for upload in uploads
    ]

@router.get("/{upload_id}")
async def get_upload_details(
    upload_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific upload
    """
    upload = db.query(UploadedData).filter(
        UploadedData.upload_id == upload_id,
        UploadedData.user_id == current_user.id
    ).first()
    
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    return {
        "upload_id": upload.upload_id,
        "file_name": upload.file_name,
        "file_size": upload.file_size,
        "total_rows": upload.total_rows,
        "total_columns": upload.total_columns,
        "column_mapping": upload.column_mapping,
        "data_summary": upload.data_summary,
        "leakage_data": upload.leakage_data,
        "status": upload.status,
        "error_message": upload.error_message,
        "created_at": upload.created_at.isoformat()
    }

def _analyze_data_for_leakages(df: pd.DataFrame, mapping: dict) -> dict:
    """
    Analyze uploaded data for potential revenue leakages
    Reads ENTIRE dataset and intelligently detects all financial columns
    """
    leakages = []
    
    # Read ALL columns and categorize them intelligently
    all_columns = df.columns.tolist()
    
    # Identify revenue-related columns (comprehensive search)
    revenue_keywords = ['revenue', 'sales', 'income', 'amount', 'total', 'price', 'value', 
                       'payment', 'receipt', 'earning', 'proceeds', 'gross', 'billing', 'invoice']
    revenue_cols = [col for col in all_columns if any(
        keyword in col.lower() for keyword in revenue_keywords
    )]
    
    # Identify cost/expense columns
    cost_keywords = ['cost', 'expense', 'spend', 'payment', 'cogs', 'overhead', 
                    'operating', 'payroll', 'rent', 'utility', 'fee', 'charge']
    cost_cols = [col for col in all_columns if any(
        keyword in col.lower() for keyword in cost_keywords
    ) and col not in revenue_cols]
    
    # Identify quantity/volume columns
    quantity_keywords = ['quantity', 'qty', 'units', 'count', 'volume', 'items']
    quantity_cols = [col for col in all_columns if any(
        keyword in col.lower() for keyword in quantity_keywords
    )]
    
    # Identify discount columns
    discount_keywords = ['discount', 'rebate', 'refund', 'return', 'credit', 'adjustment']
    discount_cols = [col for col in all_columns if any(
        keyword in col.lower() for keyword in discount_keywords
    )]
    
    # 1. ANALYZE REVENUE COLUMNS - Check for negative values (lost revenue)
    for col in revenue_cols:
        try:
            if pd.api.types.is_numeric_dtype(df[col]):
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    negative_sum = abs(df[df[col] < 0][col].sum())
                    leakages.append({
                        "id": str(uuid.uuid4())[:8],
                        "type": "Negative Revenue",
                        "column": col,
                        "description": f"Found {negative_count} negative values in '{col}' column - potential refunds, returns or data errors",
                        "amount": float(negative_sum),
                        "severity": "high",
                        "category": "Revenue Loss",
                        "status": "active",
                        "affected_rows": int(negative_count)
                    })
                
                # Check for zero values in revenue columns
                zero_count = (df[col] == 0).sum()
                if zero_count > 0:
                    leakages.append({
                        "id": str(uuid.uuid4())[:8],
                        "type": "Zero Revenue Transactions",
                        "column": col,
                        "description": f"Found {zero_count} transactions with zero revenue in '{col}' - missing pricing or free items",
                        "amount": 0,
                        "severity": "medium",
                        "category": "Pricing Issue",
                        "status": "active",
                        "affected_rows": int(zero_count)
                    })
        except Exception as e:
            print(f"Error analyzing revenue column {col}: {e}")
    
    # 2. ANALYZE COST COLUMNS - Check for excessive costs
    for col in cost_cols:
        try:
            if pd.api.types.is_numeric_dtype(df[col]):
                total_cost = df[col].sum()
                max_cost = df[col].max()
                avg_cost = df[col].mean()
                
                # Detect outlier costs (3x standard deviation)
                std_cost = df[col].std()
                outliers = df[df[col] > avg_cost + (3 * std_cost)]
                if len(outliers) > 0:
                    outlier_cost = outliers[col].sum()
                    leakages.append({
                        "id": str(uuid.uuid4())[:8],
                        "type": "Excessive Costs",
                        "column": col,
                        "description": f"Found {len(outliers)} transactions with unusually high costs in '{col}' (avg: ${avg_cost:.2f}, max: ${max_cost:.2f})",
                        "amount": float(outlier_cost),
                        "severity": "high",
                        "category": "Cost Overrun",
                        "status": "active",
                        "affected_rows": len(outliers)
                    })
        except Exception as e:
            print(f"Error analyzing cost column {col}: {e}")
    
    # 3. ANALYZE DISCOUNTS - Check for excessive discounting
    for col in discount_cols:
        try:
            if pd.api.types.is_numeric_dtype(df[col]):
                total_discount = df[col].sum()
                if total_discount > 0:
                    avg_discount = df[col].mean()
                    # Find high discounts (if there's a revenue column to compare)
                    if revenue_cols:
                        first_rev_col = next((c for c in revenue_cols if c in df.columns), None)
                        if first_rev_col:
                            discount_pct = (total_discount / df[first_rev_col].sum() * 100) if df[first_rev_col].sum() > 0 else 0
                            if discount_pct > 10:  # More than 10% discounting
                                leakages.append({
                                    "id": str(uuid.uuid4())[:8],
                                    "type": "Excessive Discounting",
                                    "column": col,
                                    "description": f"Total discounts in '{col}' represent {discount_pct:.1f}% of revenue - consider pricing strategy review",
                                    "amount": float(total_discount),
                                    "severity": "medium",
                                    "category": "Pricing Strategy",
                                    "status": "active",
                                    "affected_rows": int((df[col] > 0).sum())
                                })
        except Exception as e:
            print(f"Error analyzing discount column {col}: {e}")
    
    # 4. MISSING DATA ANALYSIS - Check ALL columns for nulls
    for col in all_columns:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            # Calculate impact if it's a financial column
            impact_amount = 0
            if col in revenue_cols and pd.api.types.is_numeric_dtype(df[col]):
                # Estimate lost revenue from missing data
                avg_value = df[col].mean()
                impact_amount = avg_value * null_count
            
            severity = "high" if col in revenue_cols else "medium" if col in cost_cols else "low"
            
            leakages.append({
                "id": str(uuid.uuid4())[:8],
                "type": "Missing Data",
                "column": col,
                "description": f"Found {null_count} missing values in '{col}' ({(null_count/len(df)*100):.1f}% of data)",
                "amount": float(impact_amount),
                "severity": severity,
                "category": "Data Quality",
                "status": "active",
                "affected_rows": int(null_count)
            })
    
    # 5. DUPLICATE DETECTION - Find duplicate transactions
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        # Try to calculate duplicate revenue
        duplicate_amount = 0
        if revenue_cols:
            first_rev_col = next((c for c in revenue_cols if c in df.columns), None)
            if first_rev_col and pd.api.types.is_numeric_dtype(df[first_rev_col]):
                duplicate_rows = df[df.duplicated(keep=False)]
                duplicate_amount = duplicate_rows[first_rev_col].sum() / 2  # Divide by 2 to avoid double counting
        
        leakages.append({
            "id": str(uuid.uuid4())[:8],
            "type": "Duplicate Transactions",
            "column": "All Columns",
            "description": f"Found {duplicate_count} duplicate rows - may indicate double billing or data entry errors",
            "amount": float(duplicate_amount),
            "severity": "high",
            "category": "Data Quality",
            "status": "active",
            "affected_rows": int(duplicate_count)
        })
    
    # 6. QUANTITY ANALYSIS - Check for negative or zero quantities
    for col in quantity_cols:
        try:
            if pd.api.types.is_numeric_dtype(df[col]):
                negative_qty = (df[col] < 0).sum()
                zero_qty = (df[col] == 0).sum()
                
                if negative_qty > 0:
                    leakages.append({
                        "id": str(uuid.uuid4())[:8],
                        "type": "Negative Quantities",
                        "column": col,
                        "description": f"Found {negative_qty} negative quantities in '{col}' - possible returns or data errors",
                        "amount": 0,
                        "severity": "medium",
                        "category": "Inventory Issue",
                        "status": "active",
                        "affected_rows": int(negative_qty)
                    })
                
                if zero_qty > 0:
                    leakages.append({
                        "id": str(uuid.uuid4())[:8],
                        "type": "Zero Quantities",
                        "column": col,
                        "description": f"Found {zero_qty} transactions with zero quantity in '{col}' - incomplete data",
                        "amount": 0,
                        "severity": "low",
                        "category": "Data Quality",
                        "status": "active",
                        "affected_rows": int(zero_qty)
                    })
        except Exception as e:
            print(f"Error analyzing quantity column {col}: {e}")
    
    # Calculate total financial impact
    total_amount = sum(l["amount"] for l in leakages)
    
    return {
        "total_leakages": len(leakages),
        "total_amount": total_amount,
        "items": leakages,
        "columns_analyzed": {
            "total_columns": len(all_columns),
            "revenue_columns": revenue_cols,
            "cost_columns": cost_cols,
            "discount_columns": discount_cols,
            "quantity_columns": quantity_cols
        }
    }

def _generate_ai_recommendations(leakage_data: dict) -> list:
    """
    Generate AI-powered recommendations based on detected leakages
    Provides specific, actionable suggestions categorized by type
    """
    recommendations = []
    
    if leakage_data["total_leakages"] == 0:
        return [
            "✅ Excellent! No critical revenue leakages detected in your data.",
            "📊 Continue monitoring your revenue streams regularly.",
            "🔍 Consider implementing automated alerts for anomaly detection.",
            "💡 Maintain data quality standards to prevent future issues."
        ]
    
    items = leakage_data.get("items", [])
    
    # Categorize leakages by type
    revenue_loss = [l for l in items if l["category"] in ["Revenue Loss", "Pricing Issue"]]
    cost_issues = [l for l in items if l["category"] == "Cost Overrun"]
    data_quality = [l for l in items if l["category"] == "Data Quality"]
    pricing_strategy = [l for l in items if l["category"] == "Pricing Strategy"]
    inventory_issues = [l for l in items if l["category"] == "Inventory Issue"]
    
    # HIGH PRIORITY - Revenue Loss Issues
    if revenue_loss:
        total_revenue_loss = sum(l["amount"] for l in revenue_loss)
        affected = sum(l.get("affected_rows", 0) for l in revenue_loss)
        recommendations.append(
            f"🚨 URGENT - Revenue Loss Detected: ${total_revenue_loss:,.2f} at risk across {affected} transactions. "
            f"Immediately review negative revenue entries and refund processes. Implement approval workflows for refunds."
        )
        recommendations.append(
            f"💰 Revenue Recovery Action: Investigate {affected} flagged transactions. "
            f"Contact customers for billing corrections where applicable. Set up automated fraud detection."
        )
    
    # COST MANAGEMENT
    if cost_issues:
        total_cost_overrun = sum(l["amount"] for l in cost_issues)
        recommendations.append(
            f"💸 Cost Control Alert: ${total_cost_overrun:,.2f} in excessive costs detected. "
            f"Review vendor contracts, negotiate better rates, and implement spending limits. "
            f"Expected savings: ${total_cost_overrun * 0.3:,.2f} (30% reduction possible)."
        )
    
    # PRICING STRATEGY
    if pricing_strategy:
        total_discounts = sum(l["amount"] for l in pricing_strategy)
        recommendations.append(
            f"📉 Pricing Strategy Review: ${total_discounts:,.2f} lost to excessive discounting. "
            f"Recommendations: 1) Cap discounts at 15% 2) Require manager approval for >10% discounts "
            f"3) Implement tiered pricing 4) Create loyalty programs instead of blanket discounts. "
            f"Potential revenue increase: ${total_discounts * 0.5:,.2f}."
        )
    
    # DATA QUALITY
    if data_quality:
        missing_data_issues = [l for l in data_quality if "Missing" in l["type"]]
        if missing_data_issues:
            total_missing = sum(l.get("affected_rows", 0) for l in missing_data_issues)
            recommendations.append(
                f"📊 Data Quality Improvement: {total_missing} records with missing data. "
                f"Actions: 1) Make critical fields mandatory 2) Implement real-time validation "
                f"3) Train staff on data entry 4) Set up automated data completeness reports. "
                f"Data quality score improvement: +{min(25, total_missing/10):.0f}%."
            )
        
        duplicate_issues = [l for l in data_quality if "Duplicate" in l["type"]]
        if duplicate_issues:
            dup_count = sum(l.get("affected_rows", 0) for l in duplicate_issues)
            recommendations.append(
                f"🔄 Duplicate Prevention: {dup_count} duplicate transactions found. "
                f"Solutions: 1) Implement unique transaction IDs 2) Enable duplicate detection in POS "
                f"3) Regular database deduplication 4) Customer notification system for duplicate charges."
            )
    
    # INVENTORY MANAGEMENT
    if inventory_issues:
        recommendations.append(
            f"📦 Inventory Control: Issues detected in quantity tracking. "
            f"Implement: 1) Barcode/RFID scanning 2) Real-time inventory sync "
            f"3) Automated reorder points 4) Monthly inventory audits. "
            f"Expected reduction in inventory errors: 80%."
        )
    
    # FINANCIAL IMPACT SUMMARY
    if leakage_data["total_amount"] > 0:
        annual_impact = leakage_data["total_amount"] * 12  # Assuming monthly data
        recommendations.append(
            f"💵 Total Financial Impact: ${leakage_data['total_amount']:,.2f} monthly, "
            f"${annual_impact:,.2f} annually. Implementing these recommendations can recover "
            f"${leakage_data['total_amount'] * 0.7:,.2f} (70% recovery rate) within 90 days."
        )
    
    # GENERAL BEST PRACTICES
    recommendations.append(
        f"🎯 Immediate Actions (Next 7 Days): "
        f"1) Review top {min(10, len(items))} flagged issues "
        f"2) Fix data entry processes "
        f"3) Set up automated monitoring alerts "
        f"4) Schedule weekly data quality reviews "
        f"5) Document standard operating procedures."
    )
    
    recommendations.append(
        f"🔧 System Improvements (Next 30 Days): "
        f"1) Implement automated validation rules "
        f"2) Upgrade to integrated accounting system "
        f"3) Train team on revenue protection "
        f"4) Set up business intelligence dashboard "
        f"5) Create exception handling workflows."
    )
    
    recommendations.append(
        f"📈 Long-term Strategy (90 Days): "
        f"1) Deploy machine learning for anomaly detection "
        f"2) Implement predictive analytics "
        f"3) Regular financial audits "
        f"4) Customer feedback loop for pricing "
        f"5) Continuous process optimization."
    )
    
    return recommendations

"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

# Enums
class BusinessStage(str, Enum):
    NEW = "new"
    EXISTING = "existing"

class BusinessModel(str, Enum):
    RETAIL = "retail"
    SAAS = "saas"
    SERVICE = "service"
    ECOMMERCE = "ecommerce"
    MANUFACTURING = "manufacturing"
    SUBSCRIPTION = "subscription"
    MARKETPLACE = "marketplace"

class PricingStrategy(str, Enum):
    COST_PLUS = "cost_plus"
    VALUE_BASED = "value_based"
    COMPETITIVE = "competitive"
    DYNAMIC = "dynamic"
    FREEMIUM = "freemium"
    TIERED = "tiered"

class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    DIGITAL_WALLET = "digital_wallet"
    CREDIT = "credit"
    SUBSCRIPTION = "subscription"

# New Business Form
class NewBusinessForm(BaseModel):
    business_name: str = Field(..., min_length=2, max_length=200)
    business_model: BusinessModel
    industry: str = Field(..., max_length=100)
    pricing_strategy: PricingStrategy
    
    # Financial projections
    expected_monthly_revenue: float = Field(..., gt=0)
    product_cost_per_unit: float = Field(..., ge=0)
    expected_units_sold: int = Field(..., gt=0)
    fixed_monthly_costs: float = Field(..., ge=0)
    
    # Pricing and discounts
    product_price: float = Field(..., gt=0)
    planned_discount_percentage: float = Field(0, ge=0, le=100)
    discount_frequency: str = "occasional"  # occasional, frequent, seasonal
    
    # Operations
    payment_methods: List[PaymentMethod]
    inventory_tracking: bool = True
    has_billing_system: bool = False
    expected_refund_rate: float = Field(0, ge=0, le=100)
    
    # Additional info
    target_market: Optional[str] = None
    competitors: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "business_name": "TechGadgets Store",
                "business_model": "ecommerce",
                "industry": "Electronics",
                "pricing_strategy": "competitive",
                "expected_monthly_revenue": 50000,
                "product_cost_per_unit": 20,
                "expected_units_sold": 1000,
                "fixed_monthly_costs": 10000,
                "product_price": 50,
                "planned_discount_percentage": 10,
                "discount_frequency": "occasional",
                "payment_methods": ["card", "digital_wallet"],
                "inventory_tracking": True,
                "has_billing_system": False,
                "expected_refund_rate": 2
            }
        }

# Existing Business Form
class ExistingBusinessForm(BaseModel):
    business_name: str = Field(..., min_length=2, max_length=200)
    business_model: BusinessModel
    industry: str = Field(..., max_length=100)
    
    # Financial data
    monthly_revenue: float = Field(..., gt=0)
    total_sales: int = Field(..., gt=0)
    total_invoices: int = Field(..., gt=0)
    
    # Revenue loss indicators
    refunds_amount: float = Field(0, ge=0)
    returns_amount: float = Field(0, ge=0)
    discounts_given: float = Field(0, ge=0)
    uncollected_payments: float = Field(0, ge=0)
    
    # Operational data
    billing_errors_count: int = Field(0, ge=0)
    pricing_inconsistencies: int = Field(0, ge=0)
    inventory_shrinkage: float = Field(0, ge=0)
    unrecorded_sales: float = Field(0, ge=0)
    
    # Product performance
    low_performing_products: int = Field(0, ge=0)
    high_cost_products: int = Field(0, ge=0)
    total_products: int = Field(..., gt=0)
    
    # Processes
    has_automated_billing: bool = False
    tracks_inventory: bool = True
    uses_crm: bool = False
    payment_methods: List[PaymentMethod]
    
    # Time period
    data_period_months: int = Field(1, ge=1, le=12)
    
    class Config:
        json_schema_extra = {
            "example": {
                "business_name": "Fashion Boutique",
                "business_model": "retail",
                "industry": "Fashion",
                "monthly_revenue": 100000,
                "total_sales": 500,
                "total_invoices": 480,
                "refunds_amount": 5000,
                "returns_amount": 3000,
                "discounts_given": 12000,
                "uncollected_payments": 2000,
                "billing_errors_count": 15,
                "pricing_inconsistencies": 8,
                "inventory_shrinkage": 4000,
                "unrecorded_sales": 1500,
                "low_performing_products": 20,
                "high_cost_products": 10,
                "total_products": 150,
                "has_automated_billing": False,
                "tracks_inventory": True,
                "uses_crm": False,
                "payment_methods": ["cash", "card"],
                "data_period_months": 3
            }
        }

# Analysis Results
class LeakagePoint(BaseModel):
    category: str
    issue: str
    estimated_loss: float
    percentage: float
    severity: str  # critical, high, medium, low
    recommendation: str

class RiskAssessment(BaseModel):
    overall_risk_score: float  # 0-100
    risk_level: str  # low, medium, high, critical
    risk_factors: List[str]
    vulnerability_areas: List[str]

class RevenueAnalysis(BaseModel):
    total_revenue: float
    estimated_leakage_amount: float
    leakage_percentage: float
    recoverable_amount: float
    leakage_points: List[LeakagePoint]
    risk_assessment: RiskAssessment
    
class RecoveryStrategy(BaseModel):
    priority_actions: List[Dict[str, Any]]
    pricing_recommendations: List[str]
    operational_improvements: List[str]
    automation_suggestions: List[str]
    cost_reduction_tips: List[str]
    revenue_growth_opportunities: List[str]
    implementation_timeline: Dict[str, List[str]]
    expected_recovery: float

class AnalysisResponse(BaseModel):
    analysis_id: str
    business_name: str
    business_stage: BusinessStage
    timestamp: datetime
    revenue_analysis: RevenueAnalysis
    recovery_strategy: RecoveryStrategy
    executive_summary: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "ANAL-2025-001",
                "business_name": "TechGadgets Store",
                "business_stage": "new",
                "timestamp": "2025-12-05T10:30:00",
                "revenue_analysis": {
                    "total_revenue": 50000,
                    "estimated_leakage_amount": 5000,
                    "leakage_percentage": 10,
                    "recoverable_amount": 4000
                },
                "executive_summary": "Analysis complete"
            }
        }

# Report Generation
class ReportRequest(BaseModel):
    analysis_id: str
    include_charts: bool = True
    include_recommendations: bool = True
    format: str = "pdf"  # pdf, json

class ReportResponse(BaseModel):
    report_id: str
    download_url: str
    generated_at: datetime

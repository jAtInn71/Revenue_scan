"""
Core business analysis service
Analyzes revenue leakage for both new and existing businesses
"""

from typing import List
from models.schemas import (
    NewBusinessForm,
    ExistingBusinessForm,
    RevenueAnalysis,
    LeakagePoint,
    RiskAssessment
)
from core.config import settings

class AnalysisService:
    """Service for analyzing business revenue leakage"""
    
    def analyze_new_business(self, form: NewBusinessForm) -> RevenueAnalysis:
        """
        Analyze potential revenue leakage risks for a NEW business
        Focuses on preventive measures and risk identification
        """
        leakage_points = []
        total_risk_score = 0
        risk_factors = []
        vulnerability_areas = []
        
        # Calculate expected revenue
        expected_revenue = form.expected_monthly_revenue
        
        # 1. Pricing Strategy Risk
        pricing_risk = self._analyze_pricing_strategy(form)
        if pricing_risk["loss"] > 0:
            leakage_points.append(LeakagePoint(**pricing_risk))
            total_risk_score += pricing_risk["percentage"]
            risk_factors.append(f"Pricing strategy ({form.pricing_strategy}) needs optimization to maximize revenue and market fit")
        
        # 2. Cost Structure Analysis
        cost_risk = self._analyze_cost_structure(form)
        if cost_risk["loss"] > 0:
            leakage_points.append(LeakagePoint(**cost_risk))
            total_risk_score += cost_risk["percentage"]
            risk_factors.append("High cost-to-revenue ratio")
        
        # 3. Discount Planning Risk
        discount_risk = self._analyze_discount_planning(form)
        if discount_risk["loss"] > 0:
            leakage_points.append(LeakagePoint(**discount_risk))
            total_risk_score += discount_risk["percentage"]
            vulnerability_areas.append("Discount management")
        
        # 4. Payment Method Risk
        payment_risk = self._analyze_payment_methods(form.payment_methods, expected_revenue)
        if payment_risk["loss"] > 0:
            leakage_points.append(LeakagePoint(**payment_risk))
            total_risk_score += payment_risk["percentage"]
            vulnerability_areas.append("Payment processing")
        
        # 5. Operational Process Risk
        operational_risk = self._analyze_operational_setup(form)
        if operational_risk["loss"] > 0:
            leakage_points.append(LeakagePoint(**operational_risk))
            total_risk_score += operational_risk["percentage"]
            vulnerability_areas.append("Operational processes")
        
        # 6. Inventory Risk (if applicable)
        if not form.inventory_tracking:
            inventory_risk = {
                "category": "Inventory Management",
                "issue": "No inventory tracking system planned",
                "description": "Without real-time inventory tracking, you risk stock discrepancies, theft, and lost sales from stockouts. This typically costs 3-5% of revenue annually.",
                "estimated_loss": expected_revenue * 0.03,
                "percentage": 3.0,
                "severity": "high",
                "recommendation": "Implement barcode/RFID inventory tracking system from day one. Use cloud-based inventory management software (like TradeGecko, Cin7, or Zoho Inventory) to prevent shrinkage, theft, and stockouts. Expected ROI: 300% in first year."
            }
            leakage_points.append(LeakagePoint(**inventory_risk))
            total_risk_score += 3.0
            vulnerability_areas.append("Inventory control")
        
        # 7. Refund Rate Risk
        if form.expected_refund_rate > 5:
            refund_risk = {
                "category": "Customer Returns",
                "issue": f"High expected refund rate: {form.expected_refund_rate}% (industry average: 2-5%)",
                "description": f"A {form.expected_refund_rate}% refund rate indicates potential issues with product quality, customer expectations, or product descriptions. Each return costs 2-3x the refund amount when including processing, restocking, and customer service.",
                "estimated_loss": expected_revenue * (form.expected_refund_rate / 100),
                "percentage": form.expected_refund_rate,
                "severity": "high" if form.expected_refund_rate > 10 else "medium",
                "recommendation": "Reduce returns to <5% by: 1) Improving product photos and descriptions, 2) Implementing quality control checks, 3) Setting clear customer expectations, 4) Analyzing return reasons to fix root causes. Target: Save $" + f"{(expected_revenue * (form.expected_refund_rate - 5) / 100):.2f}" + "/month"
            }
            leakage_points.append(LeakagePoint(**refund_risk))
            total_risk_score += form.expected_refund_rate / 2
            risk_factors.append("High refund expectations")
        
        # Calculate total leakage
        total_leakage = sum(lp.estimated_loss for lp in leakage_points)
        leakage_percentage = (total_leakage / expected_revenue * 100) if expected_revenue > 0 else 0
        
        # Normalize risk score to 0-100
        overall_risk_score = min(total_risk_score, 100)
        
        # Determine risk level
        if overall_risk_score >= settings.HIGH_RISK_THRESHOLD:
            risk_level = "critical"
        elif overall_risk_score >= settings.MEDIUM_RISK_THRESHOLD:
            risk_level = "high"
        elif overall_risk_score >= settings.LOW_RISK_THRESHOLD:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Risk assessment
        risk_assessment = RiskAssessment(
            overall_risk_score=round(overall_risk_score, 2),
            risk_level=risk_level,
            risk_factors=risk_factors if risk_factors else ["No major risk factors identified"],
            vulnerability_areas=vulnerability_areas if vulnerability_areas else ["Well-planned operations"]
        )
        
        # Calculate recoverable amount (preventable losses)
        recoverable_amount = total_leakage * 0.80  # 80% of risks are preventable
        
        return RevenueAnalysis(
            total_revenue=expected_revenue,
            estimated_leakage_amount=round(total_leakage, 2),
            leakage_percentage=round(leakage_percentage, 2),
            recoverable_amount=round(recoverable_amount, 2),
            leakage_points=leakage_points,
            risk_assessment=risk_assessment
        )
    
    def analyze_existing_business(self, form: ExistingBusinessForm) -> RevenueAnalysis:
        """
        Analyze actual revenue leakage for an EXISTING business
        Identifies current losses and recovery opportunities
        """
        leakage_points = []
        total_risk_score = 0
        risk_factors = []
        vulnerability_areas = []
        
        monthly_revenue = form.monthly_revenue
        
        # 1. Refunds and Returns
        if form.refunds_amount > 0 or form.returns_amount > 0:
            total_return_loss = form.refunds_amount + form.returns_amount
            return_percentage = (total_return_loss / monthly_revenue * 100)
            
            severity = "critical" if return_percentage > 10 else "high" if return_percentage > 5 else "medium"
            
            leakage_points.append(LeakagePoint(
                category="Refunds & Returns",
                issue=f"High return rate: ${total_return_loss:,.2f}",
                description=f"You're losing ${total_return_loss:,.2f}/month ({return_percentage:.1f}% of revenue) to refunds and returns. Each return costs 2-3x the refund amount due to restocking, processing, and lost customer lifetime value.",
                estimated_loss=total_return_loss,
                percentage=round(return_percentage, 2),
                severity=severity,
                recommendation="Analyze return reasons (quality, sizing, expectations). Improve product descriptions, add customer reviews, implement quality checks. Target: Reduce returns by 50% = Save $" + f"{total_return_loss * 0.5:,.2f}" + "/month"
            ))
            total_risk_score += return_percentage
            risk_factors.append("High customer returns")
        
        # 2. Excessive Discounts
        if form.discounts_given > monthly_revenue * 0.10:
            discount_percentage = (form.discounts_given / monthly_revenue * 100)
            
            leakage_points.append(LeakagePoint(
                category="Discount Mismanagement",
                issue=f"Excessive discounts: {discount_percentage:.1f}% of revenue",
                description=f"${form.discounts_given:,.2f}/month in discounts ({discount_percentage:.1f}% of revenue) is above healthy 5-8% range. Excessive discounting erodes brand value, trains customers to wait for sales, and destroys profit margins.",
                estimated_loss=form.discounts_given,
                percentage=round(discount_percentage, 2),
                severity="high" if discount_percentage > 15 else "medium",
                recommendation="Implement 3-tier approval: <5% (staff), 5-10% (manager), >10% (owner). Use bundling instead of discounting. Create loyalty program. Target: Reduce to 8% = Recover $" + f"{form.discounts_given - (monthly_revenue * 0.08):,.2f}" + "/month"
            ))
            total_risk_score += discount_percentage
            vulnerability_areas.append("Discount control")
        
        # 3. Billing Errors
        if form.billing_errors_count > 0:
            # Estimate average billing error at 5% of invoice value
            avg_invoice_value = monthly_revenue / form.total_invoices if form.total_invoices > 0 else 0
            billing_loss = form.billing_errors_count * avg_invoice_value * 0.05
            billing_percentage = (billing_loss / monthly_revenue * 100) if monthly_revenue > 0 else 0
            
            leakage_points.append(LeakagePoint(
                category="Billing Errors",
                issue=f"{form.billing_errors_count} billing errors detected",
                description=f"{form.billing_errors_count} billing errors/month cost ${billing_loss:,.2f} in lost revenue, write-offs, and customer disputes. Manual billing has 3-5% error rate. Each error damages customer relationships and costs time to correct.",
                estimated_loss=round(billing_loss, 2),
                percentage=round(billing_percentage, 2),
                severity="high",
                recommendation="IMMEDIATE: Switch to automated billing (QuickBooks, Xero, FreshBooks). Implement invoice review process. Set up automatic payment reminders. Expected error reduction: 95%"
            ))
            total_risk_score += billing_percentage * 2  # Billing errors are serious
            risk_factors.append("Manual billing errors")
        
        # 4. Pricing Inconsistencies
        if form.pricing_inconsistencies > 0:
            pricing_loss = monthly_revenue * 0.03  # Estimate 3% loss
            
            leakage_points.append(LeakagePoint(
                category="Pricing Errors",
                issue=f"{form.pricing_inconsistencies} pricing inconsistencies found",
                description=f"{form.pricing_inconsistencies} pricing inconsistencies across channels/locations cost ~3% revenue through undercharging, customer confusion, and margin erosion. Different prices for same product damages brand credibility.",
                estimated_loss=pricing_loss,
                percentage=3.0,
                severity="medium",
                recommendation="Audit all pricing immediately. Create centralized price list. Use POS system with synced pricing. Update all channels simultaneously. Monthly price reviews."
            ))
            total_risk_score += 3.0
            vulnerability_areas.append("Price management")
        
        # 5. Inventory Shrinkage
        if form.inventory_shrinkage > 0:
            shrinkage_percentage = (form.inventory_shrinkage / monthly_revenue * 100)
            
            leakage_points.append(LeakagePoint(
                category="Inventory Loss",
                issue=f"Inventory shrinkage: ${form.inventory_shrinkage:,.2f}",
                description=f"${form.inventory_shrinkage:,.2f}/month ({shrinkage_percentage:.1f}% of revenue) lost to theft, damage, spoilage, or counting errors. Industry average is 1.4%. This represents pure profit loss - inventory you paid for but can't sell.",
                estimated_loss=form.inventory_shrinkage,
                percentage=round(shrinkage_percentage, 2),
                severity="critical" if shrinkage_percentage > 5 else "high",
                recommendation="Install RFID/barcode tracking + security cameras. Daily cycle counts. Employee bag checks. Secure high-value items. Use shrink-wrap. Target: <1.5% shrinkage = Save $" + f"{form.inventory_shrinkage - (monthly_revenue * 0.015):,.2f}" + "/month"
            ))
            total_risk_score += shrinkage_percentage * 1.5
            risk_factors.append("Inventory theft/loss")
        
        # 6. Uncollected Payments
        if form.uncollected_payments > 0:
            uncollected_percentage = (form.uncollected_payments / monthly_revenue * 100)
            
            leakage_points.append(LeakagePoint(
                category="Uncollected Revenue",
                issue=f"Outstanding payments: ${form.uncollected_payments:,.2f}",
                description=f"${form.uncollected_payments:,.2f} in overdue receivables ({uncollected_percentage:.1f}% of revenue). After 90 days, only 50% of debts are collected. You've delivered value but aren't getting paid - this is immediate cash flow crisis.",
                estimated_loss=form.uncollected_payments,
                percentage=round(uncollected_percentage, 2),
                severity="high",
                recommendation="URGENT: Call all 30+ day accounts this week. Offer payment plans. Set up automated reminders (7, 14, 30, 60 days). Require deposits for new orders. Use payment terms: Net 15 instead of Net 30. Consider factoring for old debt."
            ))
            total_risk_score += uncollected_percentage
            vulnerability_areas.append("Payment collection")
        
        # 7. Unrecorded Sales
        if form.unrecorded_sales > 0:
            unrecorded_percentage = (form.unrecorded_sales / monthly_revenue * 100)
            
            leakage_points.append(LeakagePoint(
                category="Unrecorded Sales",
                issue=f"Missing sales records: ${form.unrecorded_sales:,.2f}",
                description=f"${form.unrecorded_sales:,.2f}/month in unrecorded sales ({unrecorded_percentage:.1f}% of revenue) = theft, forgotten charges, or system failures. This is money leaving your business without trace. Also creates tax and audit problems.",
                estimated_loss=form.unrecorded_sales,
                percentage=round(unrecorded_percentage, 2),
                severity="critical",
                recommendation="CRITICAL: Implement POS system with mandatory transaction recording (Square, Clover, Shopify POS). End-of-day reconciliation required. No manual overrides. Inventory tied to sales. Install security cameras at register."
            ))
            total_risk_score += unrecorded_percentage * 2
            risk_factors.append("Revenue leakage from unrecorded sales")
        
        # 8. Low Performing Products
        if form.low_performing_products > 0:
            product_loss_rate = form.low_performing_products / form.total_products
            estimated_loss = monthly_revenue * product_loss_rate * 0.05
            
            leakage_points.append(LeakagePoint(
                category="Product Performance",
                issue=f"{form.low_performing_products} underperforming products",
                description=f"{form.low_performing_products} out of {form.total_products} products ({product_loss_rate*100:.0f}%) are underperforming. These products consume shelf space, inventory capital, and management attention while generating minimal revenue. They hide in your sales reports costing you money.",
                estimated_loss=estimated_loss,
                percentage=round(product_loss_rate * 5, 2),
                severity="medium",
                recommendation="Run product profitability analysis (revenue - COGS - allocated costs). Discontinue bottom 20%. Reposition middle tier with new pricing/marketing. Focus resources on top 80% of revenue. Free up $" + f"{estimated_loss * 0.7:.2f}" + " in capital."
            ))
            total_risk_score += product_loss_rate * 5
        
        # 9. Process Inefficiency
        if not form.has_automated_billing:
            automation_loss = monthly_revenue * 0.02
            
            leakage_points.append(LeakagePoint(
                category="Manual Processes",
                issue="Manual billing increases error risk",
                description=f"Manual billing and invoicing costs ${automation_loss:,.2f}/month (2% revenue) in errors, forgotten invoices, late billing, and administrative time. Manual processes have 5-10x higher error rates than automated systems.",
                estimated_loss=automation_loss,
                percentage=2.0,
                severity="medium",
                recommendation="Automate billing immediately (QuickBooks, Xero, Zoho). Set up recurring invoices, automatic reminders, online payment portals. ROI: 6 months. Time saved: 10-15 hours/week."
            ))
            total_risk_score += 2.0
            vulnerability_areas.append("Process automation")
        
        # Calculate totals
        total_leakage = sum(lp.estimated_loss for lp in leakage_points)
        leakage_percentage = (total_leakage / monthly_revenue * 100) if monthly_revenue > 0 else 0
        
        # Normalize risk score
        overall_risk_score = min(total_risk_score, 100)
        
        # Determine risk level
        if overall_risk_score >= settings.HIGH_RISK_THRESHOLD:
            risk_level = "critical"
        elif overall_risk_score >= settings.MEDIUM_RISK_THRESHOLD:
            risk_level = "high"
        elif overall_risk_score >= settings.LOW_RISK_THRESHOLD:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        risk_assessment = RiskAssessment(
            overall_risk_score=round(overall_risk_score, 2),
            risk_level=risk_level,
            risk_factors=risk_factors if risk_factors else ["No major risk factors identified"],
            vulnerability_areas=vulnerability_areas if vulnerability_areas else ["Well-managed operations"]
        )
        
        # Most existing leakage is recoverable with proper actions
        recoverable_amount = total_leakage * 0.70  # 70% recoverable for existing businesses
        
        return RevenueAnalysis(
            total_revenue=monthly_revenue,
            estimated_leakage_amount=round(total_leakage, 2),
            leakage_percentage=round(leakage_percentage, 2),
            recoverable_amount=round(recoverable_amount, 2),
            leakage_points=leakage_points,
            risk_assessment=risk_assessment
        )
    
    # Helper methods for new business analysis
    
    def _analyze_pricing_strategy(self, form: NewBusinessForm) -> dict:
        """Analyze pricing strategy risks"""
        expected_revenue = form.expected_monthly_revenue
        
        # Calculate profit margin
        total_cost = (form.product_cost_per_unit * form.expected_units_sold) + form.fixed_monthly_costs
        margin = ((expected_revenue - total_cost) / expected_revenue * 100) if expected_revenue > 0 else 0
        
        # Low margin is risky
        if margin < 20:
            loss = expected_revenue * 0.05
            return {
                "category": "Pricing Strategy",
                "issue": f"Low profit margin: {margin:.1f}%",
                "description": f"Your current pricing strategy yields only {margin:.1f}% profit margin, which is below the healthy 20% threshold. This leaves little room for unexpected costs or market fluctuations.",
                "estimated_loss": loss,
                "percentage": 5.0,
                "severity": "high",
                "recommendation": "Increase prices by 10-15% or reduce COGS by negotiating better supplier terms. Target minimum 25% gross margin for sustainable business."
            }
        
        return {"loss": 0}
    
    def _analyze_cost_structure(self, form: NewBusinessForm) -> dict:
        """Analyze cost structure efficiency"""
        expected_revenue = form.expected_monthly_revenue
        total_cost = (form.product_cost_per_unit * form.expected_units_sold) + form.fixed_monthly_costs
        
        cost_ratio = (total_cost / expected_revenue) if expected_revenue > 0 else 1
        
        if cost_ratio > 0.80:  # Costs are >80% of revenue
            loss = expected_revenue * 0.08
            return {
                "category": "Cost Structure",
                "issue": f"High cost-to-revenue ratio: {cost_ratio*100:.1f}%",
                "description": f"Your costs consume {cost_ratio*100:.1f}% of revenue, leaving minimal profit. Healthy businesses maintain costs at 60-70% of revenue. This structure is financially unsustainable.",
                "estimated_loss": loss,
                "percentage": 8.0,
                "severity": "critical",
                "recommendation": "URGENT: Reduce COGS by 15-20% through supplier negotiation, bulk purchasing, or alternative suppliers. Consider price increase of 10-15%. Target: 70% cost ratio."
            }
        
        return {"loss": 0}
    
    def _analyze_discount_planning(self, form: NewBusinessForm) -> dict:
        """Analyze discount strategy risks"""
        if form.planned_discount_percentage > 15 or form.discount_frequency == "frequent":
            loss = form.expected_monthly_revenue * (form.planned_discount_percentage / 100) * 1.2
            
            return {
                "category": "Discount Strategy",
                "issue": f"Aggressive discount planning: {form.planned_discount_percentage}%",
                "description": f"Frequent discounts of {form.planned_discount_percentage}% train customers to wait for sales, eroding brand value and profit margins. Each discount dollar costs 2-3x in lost margin opportunity.",
                "estimated_loss": loss,
                "percentage": form.planned_discount_percentage * 1.2,
                "severity": "medium",
                "recommendation": "Limit discounts to 10% maximum, use strategic timing (seasonal, new customer acquisition), require manager approval for >5%, implement bundle deals instead of price cuts."
            }
        
        return {"loss": 0}
    
    def _analyze_payment_methods(self, methods: List, revenue: float) -> dict:
        """Analyze payment method risks"""
        risky_methods = ["cash", "credit"]
        
        if any(method in risky_methods for method in methods):
            loss = revenue * 0.02
            return {
                "category": "Payment Processing",
                "issue": "Cash/credit payments increase fraud risk",
                "description": "Cash and manual credit card processing lead to 2-4% revenue loss through theft, counting errors, and fraud. Digital payments provide automatic tracking and fraud protection.",
                "estimated_loss": loss,
                "percentage": 2.0,
                "severity": "medium",
                "recommendation": "Implement digital payment systems (Stripe, Square, PayPal) with automatic reconciliation. For cash, use counted till systems with dual-count procedures and daily audits."
            }
        
        return {"loss": 0}
    
    def _analyze_operational_setup(self, form: NewBusinessForm) -> dict:
        """Analyze operational process risks"""
        if not form.has_billing_system:
            loss = form.expected_monthly_revenue * 0.04
            return {
                "category": "Operational Processes",
                "issue": "No billing system planned",
                "description": "Manual billing causes 4-6% revenue loss through missed invoices, late payments, calculation errors, and forgotten charges. Automated systems ensure every transaction is captured and billed correctly.",
                "estimated_loss": loss,
                "percentage": 4.0,
                "severity": "high",
                "recommendation": "Implement cloud-based billing system (QuickBooks, FreshBooks, Zoho Books) before launch. Set up automatic invoicing, payment reminders, and late fee calculations. ROI: 500%+ in first year."
            }
        
        return {"loss": 0}

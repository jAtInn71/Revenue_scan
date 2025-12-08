"""
AI-powered recommendation service using OpenAI GPT
Generates intelligent business strategies and insights
"""

import os
from typing import Dict, List, Any
from openai import AsyncOpenAI
import json

from models.schemas import (
    NewBusinessForm,
    ExistingBusinessForm,
    RevenueAnalysis,
    RecoveryStrategy,
    BusinessStage
)
from core.config import settings

class AIService:
    """Service for AI-powered business recommendations"""
    
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "":
            try:
                self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
                self.client = None
    
    async def generate_new_business_strategy(
        self,
        form: NewBusinessForm,
        analysis: RevenueAnalysis
    ) -> RecoveryStrategy:
        """Generate AI-powered strategy for NEW businesses"""
        
        if not self.client:
            # Fallback to rule-based strategy if no AI
            return self._generate_fallback_new_strategy(form, analysis)
        
        try:
            if not self.client:
                return self._generate_fallback_new_strategy(form, analysis)
                
            prompt = self._build_new_business_prompt(form, analysis)
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a world-class business consultant and revenue optimization expert with 20+ years of experience. 
You specialize in identifying revenue leakage, preventing losses, and maximizing profitability for businesses.

Your recommendations should be:
- HIGHLY SPECIFIC and actionable (not generic advice)
- DATA-DRIVEN with clear metrics and KPIs
- PRIORITIZED by impact and urgency
- REALISTIC and implementable
- INDUSTRY-SPECIFIC based on the business context
- Include CONCRETE EXAMPLES and best practices
- Provide STEP-BY-STEP implementation guidance
- Include EXPECTED OUTCOMES and ROI estimates

Always structure your response with clear sections and bullet points for maximum readability."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=3500
            )
            
            strategy_text = response.choices[0].message.content
            
            # Parse AI response into structured strategy
            return self._parse_strategy_response(strategy_text, analysis)
            
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_fallback_new_strategy(form, analysis)
    
    async def generate_existing_business_strategy(
        self,
        form: ExistingBusinessForm,
        analysis: RevenueAnalysis
    ) -> RecoveryStrategy:
        """Generate AI-powered recovery strategy for EXISTING businesses"""
        
        try:
            if not self.client:
                return self._generate_fallback_existing_strategy(form, analysis)
                
            prompt = self._build_existing_business_prompt(form, analysis)
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a world-class business consultant and revenue recovery specialist with proven expertise in turning around struggling businesses.

Your recovery strategies should be:
- URGENCY-FOCUSED (stop the bleeding first, then optimize)
- HIGHLY SPECIFIC with exact numbers and metrics
- PRIORITIZED by immediate impact and ROI
- REALISTIC given current business constraints
- STEP-BY-STEP with clear implementation milestones
- Include QUICK WINS for immediate results
- Provide LONG-TERM strategies for sustainable growth
- Include RISK MITIGATION for each recommendation
- Specify TOOLS and RESOURCES needed
- Include SUCCESS METRICS and KPIs to track

Structure your response with clear sections, actionable items, and expected outcomes."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=3500
            )
            
            strategy_text = response.choices[0].message.content
            
            return self._parse_strategy_response(strategy_text, analysis)
            
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_fallback_existing_strategy(form, analysis)
    
    async def generate_executive_summary(
        self,
        business_name: str,
        stage: BusinessStage,
        analysis: RevenueAnalysis,
        strategy: RecoveryStrategy
    ) -> str:
        """Generate executive summary of the analysis"""
        
        summary = f"""
📊 EXECUTIVE SUMMARY - {business_name}

Revenue Health: {"⚠️ ATTENTION NEEDED" if analysis.leakage_percentage > 10 else "✅ GOOD"}
Risk Level: {analysis.risk_assessment.risk_level.upper()}

KEY FINDINGS:
• Total Revenue: ${analysis.total_revenue:,.2f}
• Estimated Leakage: ${analysis.estimated_leakage_amount:,.2f} ({analysis.leakage_percentage}%)
• Recoverable Amount: ${analysis.recoverable_amount:,.2f}
• Risk Score: {analysis.risk_assessment.overall_risk_score}/100

TOP LEAKAGE POINTS:
"""
        
        for i, lp in enumerate(analysis.leakage_points[:3], 1):
            summary += f"{i}. {lp.category}: ${lp.estimated_loss:,.2f} ({lp.percentage}%)\n"
        
        summary += f"\n💡 RECOMMENDED ACTIONS: {len(strategy.priority_actions)} priority items identified\n"
        summary += f"📈 EXPECTED RECOVERY: ${strategy.expected_recovery:,.2f}\n"
        
        return summary.strip()
    
    def _build_new_business_prompt(self, form: NewBusinessForm, analysis: RevenueAnalysis) -> str:
        """Build prompt for new business analysis"""
        
        leakage_summary = "\n".join([
            f"  • {lp.category}: ${lp.estimated_loss:,.2f} ({lp.severity} severity) - {lp.description}"
            for lp in analysis.leakage_points
        ])
        
        return f"""
🎯 MISSION: Create a comprehensive revenue protection and optimization strategy for a NEW business about to launch.

═══════════════════════════════════════════════════════
📋 BUSINESS PROFILE
═══════════════════════════════════════════════════════
Business Name: {form.business_name}
Industry: {form.industry}
Business Model: {form.business_model}
Pricing Strategy: {form.pricing_strategy}

Financial Projections:
• Expected Monthly Revenue: ${form.expected_monthly_revenue:,.2f}
• Product Price: ${form.product_price:,.2f}
• Cost per Unit: ${form.product_cost_per_unit:,.2f}
• Expected Monthly Units: {form.expected_units_sold}
• Fixed Monthly Costs: ${form.fixed_monthly_costs:,.2f}
• Planned Discount: {form.planned_discount_percentage}%
• Expected Refund Rate: {form.expected_refund_rate}%

Operational Setup:
• Payment Methods: {', '.join(form.payment_methods)}
• Inventory Tracking: {'✓ Yes' if form.inventory_tracking else '✗ No'}
• Billing System: {'✓ Yes' if form.has_billing_system else '✗ No'}
• Target Market: {form.target_market}
• Competition Level: {form.competition_level}

═══════════════════════════════════════════════════════
⚠️ IDENTIFIED REVENUE RISKS (Pre-Launch Analysis)
═══════════════════════════════════════════════════════
{leakage_summary}

📊 Risk Assessment:
• Overall Risk Score: {analysis.risk_assessment.overall_risk_score}/100
• Risk Level: {analysis.risk_assessment.risk_level.upper()}
• Potential Monthly Leakage: ${analysis.estimated_leakage_amount:,.2f}
• Leakage as % of Revenue: {analysis.leakage_percentage:.1f}%

═══════════════════════════════════════════════════════
📝 REQUIRED: COMPREHENSIVE STRATEGY OUTPUT
═══════════════════════════════════════════════════════

Please provide a DETAILED, ACTIONABLE strategy with these specific sections:

1️⃣ **CRITICAL PRE-LAUNCH ACTIONS** (5 items)
   Format for each:
   - Action: [Specific task]
   - Why Critical: [Business impact]
   - Implementation: [Step-by-step how-to]
   - Timeline: [When to complete]
   - Success Metric: [How to measure]
   - Tools Needed: [Specific tools/resources]

2️⃣ **PRICING OPTIMIZATION STRATEGY** (4-5 recommendations)
   For each recommendation:
   - Strategy: [Specific pricing tactic]
   - Expected Impact: [Revenue/margin improvement]
   - Implementation Steps: [How to execute]
   - Industry Best Practice: [Relevant example from {form.industry}]
   - Risk Mitigation: [What could go wrong and how to prevent]

3️⃣ **OPERATIONAL EXCELLENCE SETUP** (5-6 improvements)
   For each improvement:
   - Process: [What to optimize]
   - Current Gap: [What's missing]
   - Solution: [Detailed implementation]
   - Time Investment: [Hours/resources needed]
   - ROI: [Expected benefit]

4️⃣ **AUTOMATION & TECHNOLOGY STACK** (4-5 systems)
   For each system:
   - Tool Category: [Type of solution needed]
   - Recommended Tools: [2-3 specific products with why]
   - Cost Range: [Budget expectations]
   - Implementation Time: [Realistic timeline]
   - Key Features to Look For: [Must-have capabilities]

5️⃣ **COST OPTIMIZATION TACTICS** (4-5 strategies)
   For each tactic:
   - Cost Area: [Where to save]
   - Current vs Optimized: [Specific savings potential]
   - Action Plan: [How to achieve savings]
   - Trade-offs: [What to watch out for]

6️⃣ **REVENUE GROWTH ACCELERATORS** (5-6 opportunities)
   For each opportunity:
   - Growth Strategy: [Specific tactic]
   - Revenue Potential: [Estimated additional revenue]
   - Market Fit: [Why it works for {form.industry}]
   - Competitive Advantage: [How it differentiates]
   - Launch Timeline: [When to implement]

7️⃣ **90-DAY IMPLEMENTATION ROADMAP**
   Structure as:
   
   **WEEK 1-2 (Foundation):**
   - [ ] Task 1
   - [ ] Task 2
   - [ ] Task 3
   
   **WEEK 3-4 (Systems Setup):**
   - [ ] Task 1
   - [ ] Task 2
   
   **MONTH 2 (Optimization):**
   - [ ] Task 1
   - [ ] Task 2
   
   **MONTH 3 (Growth):**
   - [ ] Task 1
   - [ ] Task 2

8️⃣ **KEY PERFORMANCE INDICATORS (KPIs)**
   Define 8-10 metrics to track:
   - KPI Name: [Metric]
   - Target Value: [Goal]
   - How to Track: [Method/tool]
   - Review Frequency: [Daily/Weekly/Monthly]

9️⃣ **COMPETITIVE EDGE STRATEGIES** (for {form.competition_level} competition)
   - 3-4 specific ways to outperform competitors in {form.industry}
   - Include market positioning tactics
   - Customer retention strategies

🔟 **RISK MITIGATION PLAN**
   - Top 3 business risks and prevention strategies
   - Financial buffer recommendations
   - Contingency plans

═══════════════════════════════════════════════════════

💡 IMPORTANT: 
- Make every recommendation SPECIFIC to a {form.business_model} business in {form.industry}
- Include REAL numbers, percentages, and metrics
- Provide ACTIONABLE steps, not generic advice
- Consider the {form.competition_level} competition level
- Focus on {form.target_market} as the target market
- Account for the {form.pricing_strategy} pricing strategy

🎯 GOAL: Help this business launch successfully and avoid the most common revenue pitfalls!
"""
    
    def _build_existing_business_prompt(self, form: ExistingBusinessForm, analysis: RevenueAnalysis) -> str:
        """Build prompt for existing business analysis"""
        
        leakage_summary = "\n".join([
            f"  • {lp.category}: ${lp.estimated_loss:,.2f}/month ({lp.severity} severity)\n    → {lp.description}\n    → Impact: {lp.percentage:.1f}% of revenue\n    → Recommendation: {lp.recommendation}"
            for lp in analysis.leakage_points
        ])
        
        total_customers = form.total_customers or "Not specified"
        avg_transaction = form.average_transaction_value or "Not specified"
        
        return f"""
🚨 URGENT: Revenue Recovery Mission for Existing Business with Active Revenue Leakage

═══════════════════════════════════════════════════════
📋 BUSINESS OVERVIEW
═══════════════════════════════════════════════════════
Business Name: {form.business_name}
Industry: {form.industry}
Business Model: {form.business_model}
Time in Business: {form.years_in_business} years

Current Financial Status:
• Monthly Revenue: ${form.monthly_revenue:,.2f}
• Total Customers: {total_customers}
• Average Transaction: ${avg_transaction if isinstance(avg_transaction, (int, float)) else 'N/A'}
• Billing Issues: {'✓ Yes - CRITICAL' if form.has_billing_issues else '✓ None reported'}
• Inventory Issues: {'✓ Yes - ATTENTION NEEDED' if form.has_inventory_issues else '✓ Under control'}
• Pricing Inconsistencies: {'✓ Yes - REVENUE LEAK' if form.has_pricing_inconsistencies else '✓ Consistent'}

═══════════════════════════════════════════════════════
💰 DETECTED REVENUE LEAKAGE (Active Losses)
═══════════════════════════════════════════════════════
{leakage_summary}

📊 Financial Impact Analysis:
• Total Monthly Revenue Loss: ${analysis.estimated_leakage_amount:,.2f}
• Leakage as % of Revenue: {analysis.leakage_percentage:.1f}%
• ANNUAL IMPACT: ${analysis.estimated_leakage_amount * 12:,.2f}
• Immediately Recoverable: ${analysis.recoverable_amount:,.2f}
• Risk Score: {analysis.risk_assessment.overall_risk_score}/100 ({analysis.risk_assessment.risk_level.upper()} RISK)

⚠️ This represents ${analysis.estimated_leakage_amount * 12:,.2f} in lost annual revenue that should be in your bank account!

═══════════════════════════════════════════════════════
📝 REQUIRED: COMPREHENSIVE RECOVERY STRATEGY
═══════════════════════════════════════════════════════

Provide a DETAILED, IMMEDIATELY ACTIONABLE recovery plan with these sections:

1️⃣ **EMERGENCY ACTIONS** (Next 48-72 Hours - Stop the Bleeding)
   For each action (5 items):
   - URGENT Action: [What to do RIGHT NOW]
   - Why This Matters: [Immediate financial impact]
   - Quick Implementation: [Can be done this week]
   - Who Should Do It: [Role/person responsible]
   - Expected Immediate Savings: [Dollar amount]
   - Success Indicator: [How you'll know it worked]

2️⃣ **REVENUE RECOVERY PLAN** (First 30 Days)
   For each strategy (5-6 items):
   - Recovery Tactic: [Specific action]
   - Target Amount: [How much revenue to recover]
   - Step-by-Step Process: [Detailed implementation]
   - Tools/Resources Needed: [What you need]
   - Timeline: [Days to implementation]
   - Risk Level: [What could go wrong]
   - Mitigation: [How to handle issues]

3️⃣ **PRICING CORRECTION STRATEGY**
   For each recommendation (4-5 items):
   - Current Problem: [What's wrong with pricing]
   - Financial Impact: [How much it's costing]
   - Corrective Action: [How to fix it]
   - Price Point Recommendation: [Specific numbers]
   - Customer Communication Plan: [How to explain changes]
   - Expected Revenue Lift: [Percentage improvement]

4️⃣ **OPERATIONAL FIXES** (Process Improvements)
   For each improvement (5-6 items):
   - Broken Process: [What's not working]
   - Current Cost: [Impact in dollars]
   - Solution: [How to fix it permanently]
   - Implementation Difficulty: [Easy/Medium/Hard]
   - Time to Implement: [Realistic timeline]
   - Annual Savings: [Long-term financial benefit]

5️⃣ **TECHNOLOGY UPGRADES** (Systems to Stop Leaks)
   For each system (4-5 items):
   - System Type: [What you need]
   - Current Gap: [What's missing]
   - Top 3 Tool Recommendations: [Specific products for {form.industry}]
   - Price Range: [Investment required]
   - ROI Timeline: [When you'll break even]
   - Integration Requirements: [What it needs to work with]
   - Expected Leakage Reduction: [How much it will save]

6️⃣ **COST REDUCTION ROADMAP** (Immediate Savings)
   For each opportunity (5 items):
   - Cost Category: [What you're overspending on]
   - Current Monthly Cost: [Estimate if known]
   - Optimization Strategy: [How to reduce]
   - Potential Monthly Savings: [Dollar amount]
   - Implementation Steps: [Action plan]
   - Trade-offs: [What you might sacrifice]

7️⃣ **REVENUE GROWTH OPPORTUNITIES** (Beyond Recovery)
   For each opportunity (5-6 items):
   - Growth Strategy: [Specific tactic]
   - Revenue Potential: [Additional monthly revenue]
   - Why It Works for {form.industry}: [Market reasoning]
   - Customer Segment: [Who to target]
   - Launch Timeline: [When to start]
   - Required Investment: [Time and money needed]
   - Competitive Analysis: [How it positions you]

8️⃣ **120-DAY RECOVERY ROADMAP**

   **WEEK 1 (Emergency Stabilization):**
   - [ ] Stop critical leaks
   - [ ] Implement emergency fixes
   - [ ] Set up tracking systems
   
   **WEEKS 2-4 (Quick Wins):**
   - [ ] Revenue recovery actions
   - [ ] Pricing corrections
   - [ ] Process fixes
   
   **MONTH 2 (System Implementation):**
   - [ ] Technology upgrades
   - [ ] Staff training
   - [ ] Process documentation
   
   **MONTH 3 (Optimization):**
   - [ ] Fine-tune systems
   - [ ] Monitor metrics
   - [ ] Adjust strategy
   
   **MONTH 4 (Growth Mode):**
   - [ ] Launch growth initiatives
   - [ ] Expand successful tactics
   - [ ] Scale operations

9️⃣ **FINANCIAL RECOVERY PROJECTIONS**
   Provide month-by-month recovery estimates:
   - Month 1: $[amount] recovered
   - Month 2: $[amount] recovered
   - Month 3: $[amount] recovered
   - Month 4: $[amount] recovered
   - Total 4-Month Recovery: $[total]
   - Annualized Impact: $[yearly amount]

🔟 **CRITICAL KPIs TO TRACK DAILY**
   Define 10-12 metrics with:
   - KPI Name: [Metric]
   - Current Value: [Baseline]
   - Target Value: [Goal]
   - Tracking Method: [How to measure]
   - Alert Threshold: [When to take action]
   - Review Frequency: [How often to check]

1️⃣1️⃣ **QUICK WIN OPPORTUNITIES** (Easiest to Implement)
   - 5 actions that can be done THIS WEEK
   - Each with specific dollar value impact
   - Prioritized by ease vs. impact

1️⃣2️⃣ **RISK MITIGATION & CONTINGENCY PLANS**
   - What if recovery is slower than expected?
   - What if customers resist pricing changes?
   - What if new systems fail?
   - Backup plans for each scenario

═══════════════════════════════════════════════════════

💡 CRITICAL CONTEXT:
- This is a {form.years_in_business}-year-old {form.business_model} business in {form.industry}
- Currently losing ${analysis.estimated_leakage_amount:,.2f}/month (${analysis.estimated_leakage_amount * 12:,.2f}/year!)
- Recommendations must be IMMEDIATELY ACTIONABLE
- Focus on QUICK WINS for momentum
- Provide EXACT NUMBERS and SPECIFIC TOOLS
- Every recommendation should have clear ROI
- This business needs to recover ${analysis.recoverable_amount:,.2f} ASAP

🎯 PRIMARY GOAL: Stop revenue leakage immediately and recover lost revenue within 120 days!
🏆 SECONDARY GOAL: Build systems to prevent future leakage and enable sustainable growth!
"""
    
    def _parse_strategy_response(self, ai_response: str, analysis: RevenueAnalysis) -> RecoveryStrategy:
        """Parse AI response into structured RecoveryStrategy"""
        
        # Simple parsing - in production, use more sophisticated parsing
        lines = ai_response.split('\n')
        
        priority_actions = []
        pricing_recs = []
        operational = []
        automation = []
        cost_reduction = []
        growth_ops = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            if "priority" in line.lower() or "immediate" in line.lower():
                current_section = "priority"
            elif "pricing" in line.lower():
                current_section = "pricing"
            elif "operational" in line.lower() or "process" in line.lower():
                current_section = "operational"
            elif "automation" in line.lower() or "system" in line.lower():
                current_section = "automation"
            elif "cost" in line.lower() or "reduce" in line.lower():
                current_section = "cost"
            elif "growth" in line.lower() or "opportunity" in line.lower():
                current_section = "growth"
            
            # Add to appropriate section
            if line.startswith(('-', '•', '*', '1.', '2.', '3.', '4.', '5.')):
                clean_line = line.lstrip('-•*123456789. ')
                
                if current_section == "priority" and len(priority_actions) < 5:
                    priority_actions.append({
                        "action": clean_line,
                        "priority": "high",
                        "timeline": "immediate"
                    })
                elif current_section == "pricing" and len(pricing_recs) < 4:
                    pricing_recs.append(clean_line)
                elif current_section == "operational" and len(operational) < 5:
                    operational.append(clean_line)
                elif current_section == "automation" and len(automation) < 4:
                    automation.append(clean_line)
                elif current_section == "cost" and len(cost_reduction) < 4:
                    cost_reduction.append(clean_line)
                elif current_section == "growth" and len(growth_ops) < 4:
                    growth_ops.append(clean_line)
        
        # Implementation timeline
        timeline = {
            "immediate": [pa["action"] for pa in priority_actions[:2]],
            "30_days": [pa["action"] for pa in priority_actions[2:4]],
            "60_days": operational[:2] if operational else ["Review and optimize"],
            "90_days": growth_ops[:2] if growth_ops else ["Expand operations"]
        }
        
        return RecoveryStrategy(
            priority_actions=priority_actions if priority_actions else self._get_default_actions(analysis),
            pricing_recommendations=pricing_recs if pricing_recs else self._get_default_pricing_recs(),
            operational_improvements=operational if operational else self._get_default_operational(),
            automation_suggestions=automation if automation else self._get_default_automation(),
            cost_reduction_tips=cost_reduction if cost_reduction else self._get_default_cost_tips(),
            revenue_growth_opportunities=growth_ops if growth_ops else self._get_default_growth_ops(),
            implementation_timeline=timeline,
            expected_recovery=analysis.recoverable_amount
        )
    
    def _generate_fallback_new_strategy(self, form: NewBusinessForm, analysis: RevenueAnalysis) -> RecoveryStrategy:
        """Generate rule-based strategy for new businesses (fallback)"""
        
        priority_actions = [
            {
                "action": "Set up automated billing system before launch",
                "priority": "critical",
                "timeline": "before_launch"
            },
            {
                "action": "Implement inventory tracking from day one",
                "priority": "high",
                "timeline": "before_launch"
            },
            {
                "action": "Establish clear pricing policy across all channels",
                "priority": "high",
                "timeline": "week_1"
            },
            {
                "action": "Create discount approval workflow",
                "priority": "medium",
                "timeline": "week_2"
            },
            {
                "action": "Set up payment processing with fraud protection",
                "priority": "high",
                "timeline": "before_launch"
            }
        ]
        
        pricing_recs = [
            f"Ensure minimum 25% profit margin on all products",
            f"Review pricing against competitors in {form.industry}",
            "Implement dynamic pricing for high-demand periods",
            "Bundle products to increase average transaction value"
        ]
        
        operational = [
            "Automate invoice generation and delivery",
            "Implement real-time inventory management",
            "Set up customer relationship management (CRM) system",
            "Create standard operating procedures for all processes",
            "Train staff on revenue protection best practices"
        ]
        
        automation = [
            "Use cloud-based accounting software (QuickBooks, Xero)",
            "Implement point-of-sale system with analytics",
            "Set up automated payment reminders",
            "Use inventory management software with alerts"
        ]
        
        cost_reduction = [
            "Negotiate better terms with suppliers",
            "Optimize inventory levels to reduce holding costs",
            "Consider dropshipping for low-volume items",
            "Use energy-efficient equipment to reduce utilities"
        ]
        
        growth_ops = [
            "Implement customer loyalty program",
            "Create upsell and cross-sell strategies",
            "Expand to online sales channels",
            "Develop subscription or recurring revenue model"
        ]
        
        timeline = {
            "immediate": ["Set up billing system", "Establish pricing policy"],
            "30_days": ["Implement inventory tracking", "Train staff"],
            "60_days": ["Launch loyalty program", "Optimize processes"],
            "90_days": ["Expand sales channels", "Review and adjust strategy"]
        }
        
        return RecoveryStrategy(
            priority_actions=priority_actions,
            pricing_recommendations=pricing_recs,
            operational_improvements=operational,
            automation_suggestions=automation,
            cost_reduction_tips=cost_reduction,
            revenue_growth_opportunities=growth_ops,
            implementation_timeline=timeline,
            expected_recovery=analysis.recoverable_amount
        )
    
    def _generate_fallback_existing_strategy(self, form: ExistingBusinessForm, analysis: RevenueAnalysis) -> RecoveryStrategy:
        """Generate rule-based strategy for existing businesses (fallback)"""
        
        priority_actions = []
        
        # Prioritize based on biggest leaks
        top_leaks = sorted(analysis.leakage_points, key=lambda x: x.estimated_loss, reverse=True)
        
        for leak in top_leaks[:5]:
            priority_actions.append({
                "action": f"Address {leak.category}: {leak.recommendation}",
                "priority": leak.severity,
                "timeline": "immediate" if leak.severity == "critical" else "this_week",
                "expected_savings": leak.estimated_loss * 0.7
            })
        
        pricing_recs = [
            "Conduct pricing audit across all products and channels",
            "Eliminate pricing inconsistencies",
            "Review and justify all discounts given",
            "Implement price optimization based on demand"
        ]
        
        operational = [
            "Automate billing to eliminate manual errors",
            "Implement strict discount approval process",
            "Set up automated payment collection and reminders",
            "Conduct regular inventory audits",
            "Implement quality control to reduce returns"
        ]
        
        automation = [
            "Upgrade to automated billing system",
            "Implement CRM with payment tracking",
            "Use RFID or barcode for inventory management",
            "Set up business intelligence dashboard"
        ]
        
        cost_reduction = [
            "Eliminate or reposition underperforming products",
            "Renegotiate supplier contracts",
            "Reduce inventory holding costs",
            "Optimize staffing based on demand patterns"
        ]
        
        growth_ops = [
            "Recover uncollected payments through follow-up",
            "Convert returned customers with targeted offers",
            "Capture all sales through improved POS",
            "Increase average order value through bundling"
        ]
        
        timeline = {
            "immediate": [pa["action"] for pa in priority_actions if pa["priority"] == "critical"],
            "this_week": [pa["action"] for pa in priority_actions if pa["priority"] == "high"][:2],
            "30_days": operational[:2],
            "60_days": growth_ops[:2]
        }
        
        return RecoveryStrategy(
            priority_actions=priority_actions,
            pricing_recommendations=pricing_recs,
            operational_improvements=operational,
            automation_suggestions=automation,
            cost_reduction_tips=cost_reduction,
            revenue_growth_opportunities=growth_ops,
            implementation_timeline=timeline,
            expected_recovery=analysis.recoverable_amount
        )
    
    # Default recommendations helpers
    def _get_default_actions(self, analysis: RevenueAnalysis) -> List[Dict[str, Any]]:
        return [
            {"action": lp.recommendation, "priority": lp.severity, "timeline": "immediate"}
            for lp in analysis.leakage_points[:5]
        ]
    
    def _get_default_pricing_recs(self) -> List[str]:
        return [
            "Review and optimize pricing strategy",
            "Implement dynamic pricing where applicable",
            "Ensure consistent pricing across channels"
        ]
    
    def _get_default_operational(self) -> List[str]:
        return [
            "Automate manual processes",
            "Implement quality control measures",
            "Train staff on best practices"
        ]
    
    def _get_default_automation(self) -> List[str]:
        return [
            "Implement automated billing system",
            "Use inventory management software",
            "Set up business analytics dashboard"
        ]
    
    def _get_default_cost_tips(self) -> List[str]:
        return [
            "Negotiate better supplier terms",
            "Optimize inventory levels",
            "Reduce operational waste"
        ]
    
    def _get_default_growth_ops(self) -> List[str]:
        return [
            "Expand to new sales channels",
            "Implement customer loyalty program",
            "Optimize product mix"
        ]
    
    async def generate_chat_response(self, user_message: str, context: dict) -> dict:
        """
        Generate AI chat response for revenue insights
        """
        if not self.client:
            return self._generate_fallback_chat_response(user_message, context)
        
        try:
            # Build context string
            context_str = f"""
Company: {context['user'].get('company', 'N/A')}
Recent Revenue: ${sum(a.get('total_revenue', 0) for a in context.get('recent_analyses', [])):,.2f}
Recent Leakage: ${sum(a.get('leakage_amount', 0) for a in context.get('recent_analyses', [])):,.2f}
"""
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a Revenue Leakage Analysis AI Assistant. You help finance managers and business analysts identify, prevent, and recover lost revenue.

Provide:
- Clear, actionable insights
- Specific numbers and metrics
- Step-by-step recommendations
- Industry best practices

Always structure responses with:
1. Direct answer to the question
2. Key drivers/factors (2-4 points)
3. Suggested actions (3-5 items)

Be professional but friendly. Use data from the context when available."""
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{context_str}\n\nQuestion: {user_message}"
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            
            # Try to extract structured data
            return {
                "content": content,
                "key_drivers": self._extract_key_points(content),
                "suggested_actions": self._extract_actions(content)
            }
            
        except Exception as e:
            print(f"AI chat failed: {e}")
            return self._generate_fallback_chat_response(user_message, context)
    
    async def explain_leakage_data(self, leakage_data: dict, business_context: dict) -> dict:
        """
        Explain detected leakages using AI
        """
        if not self.client or not leakage_data:
            return {
                "content": "Analysis complete. Please review the detected leakage points.",
                "recommendations": ["Review data quality", "Implement validation checks"]
            }
        
        try:
            items = leakage_data.get("items", [])
            total = leakage_data.get("total_amount", 0)
            
            prompt = f"""
Analyze these revenue leakages detected in {business_context.get('file_name', 'uploaded data')}:

Total Leakages: {len(items)}
Total Amount: ${total:,.2f}

Issues found:
{json.dumps(items[:5], indent=2)}

Provide:
1. Brief explanation of the issues
2. Severity assessment
3. Top 3 recommendations to fix
"""
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data quality and revenue analyst. Explain issues clearly and provide actionable fixes."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.6,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            
            return {
                "content": content,
                "recommendations": self._extract_actions(content),
                "severity_analysis": {
                    "high": len([i for i in items if i.get("severity") == "high"]),
                    "medium": len([i for i in items if i.get("severity") == "medium"]),
                    "low": len([i for i in items if i.get("severity") == "low"])
                }
            }
            
        except Exception as e:
            print(f"AI explanation failed: {e}")
            return {
                "content": "Data quality issues detected. Review highlighted items.",
                "recommendations": ["Fix data entry processes", "Add validation rules", "Regular data audits"]
            }
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key points from AI response"""
        points = []
        for line in text.split('\n'):
            if any(line.strip().startswith(prefix) for prefix in ['•', '-', '*', '1.', '2.', '3.']):
                clean = line.strip().lstrip('•-*123456789. ')
                if len(clean) > 10 and len(clean) < 150:
                    points.append(clean)
        return points[:4]
    
    def _extract_actions(self, text: str) -> List[str]:
        """Extract action items from AI response"""
        actions = []
        in_actions = False
        
        for line in text.split('\n'):
            if any(word in line.lower() for word in ['action', 'recommend', 'next step', 'should']):
                in_actions = True
            
            if in_actions and any(line.strip().startswith(p) for p in ['•', '-', '*', '1.', '2.', '3.']):
                clean = line.strip().lstrip('•-*123456789. ')
                if len(clean) > 10:
                    actions.append(clean)
        
        return actions[:5] if actions else [
            "Review dashboard metrics",
            "Upload transaction data",
            "Set up automated alerts"
        ]
    
    def _generate_fallback_chat_response(self, message: str, context: dict) -> dict:
        """Fallback response when AI unavailable"""
        return {
            "content": "I'm here to help analyze your revenue data. Try uploading your transaction data or asking about specific metrics.",
            "key_drivers": ["Data analysis", "Pattern detection", "Actionable insights"],
            "suggested_actions": ["Upload CSV data", "Review dashboard", "Set up alerts"]
        }
    
    async def analyze_full_dataset(self, df, file_name: str, leakage_data: dict) -> dict:
        """
        Perform comprehensive AI analysis of uploaded dataset
        Analyzes ALL columns, calculates financial metrics, and provides detailed insights
        """
        if not self.client:
            return self._generate_fallback_dataset_analysis(df, leakage_data)
        
        try:
            import pandas as pd
            
            # Comprehensive data analysis
            total_rows = len(df)
            total_columns = len(df.columns)
            
            # Identify all column types
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            # Calculate key financial metrics
            revenue_cols = [col for col in numeric_cols if any(term in col.lower() for term in 
                           ['revenue', 'sales', 'amount', 'total', 'price', 'income', 'profit'])]
            
            cost_cols = [col for col in numeric_cols if any(term in col.lower() for term in 
                        ['cost', 'expense', 'cogs', 'spend', 'payment'])]
            
            # Financial summary
            total_revenue = sum(df[col].sum() for col in revenue_cols if col in df.columns)
            total_costs = sum(df[col].sum() for col in cost_cols if col in df.columns)
            total_profit = total_revenue - total_costs
            
            # Column statistics
            column_stats = {}
            for col in numeric_cols[:20]:  # Limit to first 20 numeric columns
                column_stats[col] = {
                    "mean": float(df[col].mean()) if not df[col].isna().all() else 0,
                    "sum": float(df[col].sum()) if not df[col].isna().all() else 0,
                    "min": float(df[col].min()) if not df[col].isna().all() else 0,
                    "max": float(df[col].max()) if not df[col].isna().all() else 0,
                    "null_count": int(df[col].isnull().sum())
                }
            
            # Prepare prompt
            prompt = f"""Analyze this financial dataset:

DATA OVERVIEW:
- Rows: {total_rows:,}, Columns: {total_columns}
- Revenue: ${total_revenue:,.2f}
- Costs: ${total_costs:,.2f}  
- Profit: ${total_profit:,.2f}

COLUMNS: {', '.join(df.columns.tolist()[:30])}

LEAKAGES: {leakage_data.get('total_leakages', 0)} issues, ${leakage_data.get('total_amount', 0):,.2f} at risk

Provide:
1. Executive summary (3 sentences)
2. Revenue analysis (4 key insights)
3. Profit & loss insights (3 points)
4. Leakage assessment (4 findings)
5. Top 5 actionable recommendations with $ impact
6. KPIs: revenue/transaction, profit margin, data quality score
7. 30-day action plan

Use specific numbers. Be concise and actionable."""
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a financial analyst. Provide data-driven, actionable insights with specific numbers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            ai_insights = response.choices[0].message.content
            
            return {
                "status": "completed",
                "message": f"Analyzed {total_rows:,} rows across {total_columns} columns",
                "financial_summary": {
                    "total_revenue": total_revenue,
                    "total_costs": total_costs,
                    "net_profit": total_profit,
                    "profit_margin": (total_profit/total_revenue*100) if total_revenue > 0 else 0
                },
                "ai_insights": ai_insights,
                "recommendations": self._extract_actions(ai_insights),
                "kpis": {
                    "revenue_per_transaction": total_revenue / total_rows if total_rows > 0 else 0,
                    "total_transactions": total_rows,
                    "revenue_at_risk": leakage_data.get('total_amount', 0)
                }
            }
            
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return self._generate_fallback_dataset_analysis(df, leakage_data)
    
    def _generate_fallback_dataset_analysis(self, df, leakage_data: dict) -> dict:
        """Generate basic analysis when AI is unavailable"""
        total_rows = len(df)
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        revenue_cols = [col for col in numeric_cols if any(term in col.lower() for term in 
                       ['revenue', 'sales', 'amount', 'total', 'price'])]
        
        total_revenue = sum(df[col].sum() for col in revenue_cols if col in df.columns)
        
        return {
            "status": "completed",
            "message": f"Analyzed {total_rows:,} rows",
            "financial_summary": {
                "total_revenue": total_revenue,
                "total_costs": 0,
                "net_profit": 0,
                "profit_margin": 0
            },
            "ai_insights": f"Dataset contains {total_rows:,} transactions with ${total_revenue:,.2f} in revenue. {leakage_data.get('total_leakages', 0)} issues detected requiring review.",
            "recommendations": [
                "Review flagged transactions",
                "Implement data validation",
                "Set up monitoring alerts",
                "Conduct regular audits",
                "Train team on accuracy"
            ],
            "kpis": {
                "revenue_per_transaction": total_revenue / total_rows if total_rows > 0 else 0,
                "total_transactions": total_rows,
                "revenue_at_risk": leakage_data.get('total_amount', 0)
            }
        }

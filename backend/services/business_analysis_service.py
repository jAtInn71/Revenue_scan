from datetime import datetime
from typing import Dict, Any, List
from openai import AsyncOpenAI
from core.config import settings

class BusinessAnalysisService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
    async def analyze_new_business(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a new business proposal and identify potential revenue leaks before launch
        """
        # Extract form data
        business_name = form_data.get('business_name', 'Your Business')
        industry = form_data.get('industry', 'N/A')
        business_model = form_data.get('business_model', 'N/A')
        pricing_strategy = form_data.get('pricing_strategy', 'N/A')
        expected_monthly_revenue = float(form_data.get('expected_monthly_revenue', 0))
        product_price = float(form_data.get('product_price', 0))
        product_cost_per_unit = float(form_data.get('product_cost_per_unit', 0))
        expected_units_sold = int(form_data.get('expected_units_sold', 0))
        fixed_monthly_costs = float(form_data.get('fixed_monthly_costs', 0))
        planned_discount_percentage = float(form_data.get('planned_discount_percentage', 0))
        expected_refund_rate = float(form_data.get('expected_refund_rate', 0))
        payment_methods = form_data.get('payment_methods', [])
        inventory_tracking = form_data.get('inventory_tracking', False)
        has_billing_system = form_data.get('has_billing_system', False)
        
        # Calculate potential revenue and costs
        gross_revenue = product_price * expected_units_sold
        total_costs = (product_cost_per_unit * expected_units_sold) + fixed_monthly_costs
        discount_loss = gross_revenue * (planned_discount_percentage / 100)
        refund_loss = gross_revenue * (expected_refund_rate / 100)
        net_revenue = gross_revenue - discount_loss - refund_loss - total_costs
        
        # Identify leakage points
        leakage_points = []
        
        # Check pricing strategy risks
        if pricing_strategy == 'cost_plus' and product_price <= product_cost_per_unit * 1.2:
            leakage_points.append({
                'category': 'Pricing',
                'severity': 'high',
                'description': 'Low profit margin detected',
                'impact': f'${(product_price - product_cost_per_unit) * expected_units_sold:.2f}',
                'recommendation': 'Consider value-based pricing to increase margins'
            })
            
        # Check discount strategy
        if planned_discount_percentage > 15:
            leakage_points.append({
                'category': 'Discounts',
                'severity': 'medium',
                'description': 'High planned discount rate',
                'impact': f'${discount_loss:.2f}/month',
                'recommendation': 'Implement tiered discounts and limit promotional periods'
            })
            
        # Check refund expectations
        if expected_refund_rate > 5:
            leakage_points.append({
                'category': 'Refunds',
                'severity': 'high',
                'description': 'High expected refund rate',
                'impact': f'${refund_loss:.2f}/month',
                'recommendation': 'Improve product descriptions and set clear return policies'
            })
            
        # Check billing system
        if not has_billing_system:
            estimated_billing_errors = expected_units_sold * 0.03  # 3% error rate
            leakage_points.append({
                'category': 'Billing',
                'severity': 'high',
                'description': 'No automated billing system',
                'impact': f'~{estimated_billing_errors:.0f} potential billing errors/month',
                'recommendation': 'Implement automated billing software to reduce human errors'
            })
            
        # Check inventory tracking
        if not inventory_tracking:
            leakage_points.append({
                'category': 'Inventory',
                'severity': 'medium',
                'description': 'No inventory tracking system',
                'impact': 'Risk of stockouts and overselling',
                'recommendation': 'Implement inventory management system to prevent losses'
            })
            
        # Check payment methods
        if len(payment_methods) < 2:
            leakage_points.append({
                'category': 'Payments',
                'severity': 'low',
                'description': 'Limited payment options',
                'impact': 'Potential lost sales due to payment friction',
                'recommendation': 'Add more payment methods to reduce cart abandonment'
            })
            
        # Generate AI-powered recovery strategies
        recovery_strategies = await self._generate_recovery_strategies(
            business_name, 
            industry, 
            business_model,
            leakage_points
        )
        
        # Risk assessment
        risk_level = self._calculate_risk_level(leakage_points)
        
        # Executive summary
        total_potential_loss = discount_loss + refund_loss
        
        return {
            'analysis_id': f'NEW_{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'business_name': business_name,
            'analysis_type': 'new_business',
            'analysis_date': datetime.now().isoformat(),
            'financial_summary': {
                'expected_monthly_revenue': expected_monthly_revenue,
                'gross_revenue': gross_revenue,
                'total_costs': total_costs,
                'discount_loss': discount_loss,
                'refund_loss': refund_loss,
                'net_revenue': net_revenue,
                'profit_margin': ((net_revenue / gross_revenue) * 100) if gross_revenue > 0 else 0
            },
            'leakage_points': leakage_points,
            'leakage_count': len(leakage_points),
            'total_potential_loss': total_potential_loss,
            'risk_level': risk_level,
            'recovery_strategies': recovery_strategies,
            'executive_summary': f"{business_name} shows {risk_level} risk with {len(leakage_points)} potential leakage points identified. Total estimated monthly loss: ${total_potential_loss:.2f}."
        }
        
    async def analyze_existing_business(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an existing business and identify actual revenue leaks
        """
        # Extract form data
        business_name = form_data.get('business_name', 'Your Business')
        industry = form_data.get('industry', 'N/A')
        business_model = form_data.get('business_model', 'N/A')
        monthly_revenue = float(form_data.get('monthly_revenue', 0))
        total_sales = int(form_data.get('total_sales', 0))
        total_invoices = int(form_data.get('total_invoices', 0))
        refunds_amount = float(form_data.get('refunds_amount', 0))
        returns_amount = float(form_data.get('returns_amount', 0))
        discounts_given = float(form_data.get('discounts_given', 0))
        uncollected_payments = float(form_data.get('uncollected_payments', 0))
        billing_errors_count = int(form_data.get('billing_errors_count', 0))
        pricing_inconsistencies = int(form_data.get('pricing_inconsistencies', 0))
        inventory_shrinkage = float(form_data.get('inventory_shrinkage', 0))
        unrecorded_sales = float(form_data.get('unrecorded_sales', 0))
        low_performing_products = int(form_data.get('low_performing_products', 0))
        high_cost_products = int(form_data.get('high_cost_products', 0))
        total_products = int(form_data.get('total_products', 0))
        has_automated_billing = form_data.get('has_automated_billing', False)
        tracks_inventory = form_data.get('tracks_inventory', False)
        uses_crm = form_data.get('uses_crm', False)
        data_period_months = int(form_data.get('data_period_months', 3))
        
        # Calculate total revenue loss
        total_loss = (refunds_amount + returns_amount + discounts_given + 
                     uncollected_payments + inventory_shrinkage + unrecorded_sales)
        
        # Calculate percentages
        refund_rate = (refunds_amount / monthly_revenue * 100) if monthly_revenue > 0 else 0
        discount_rate = (discounts_given / monthly_revenue * 100) if monthly_revenue > 0 else 0
        invoice_gap = total_sales - total_invoices
        
        # Identify leakage points
        leakage_points = []
        
        # Refunds analysis
        if refund_rate > 5:
            leakage_points.append({
                'category': 'Refunds',
                'severity': 'high' if refund_rate > 10 else 'medium',
                'description': f'High refund rate ({refund_rate:.1f}%)',
                'impact': f'${refunds_amount:.2f}',
                'recommendation': 'Investigate root causes of refunds and improve quality control'
            })
            
        # Returns analysis
        if returns_amount > monthly_revenue * 0.05:
            leakage_points.append({
                'category': 'Returns',
                'severity': 'medium',
                'description': f'Significant returns ({returns_amount / monthly_revenue * 100:.1f}%)',
                'impact': f'${returns_amount:.2f}',
                'recommendation': 'Review product descriptions and set realistic expectations'
            })
            
        # Discounts analysis
        if discount_rate > 15:
            leakage_points.append({
                'category': 'Discounts',
                'severity': 'high' if discount_rate > 20 else 'medium',
                'description': f'Excessive discounts ({discount_rate:.1f}%)',
                'impact': f'${discounts_given:.2f}',
                'recommendation': 'Implement strategic discount policies and reduce blanket discounts'
            })
            
        # Uncollected payments
        if uncollected_payments > 0:
            leakage_points.append({
                'category': 'Collections',
                'severity': 'high',
                'description': f'Uncollected payments',
                'impact': f'${uncollected_payments:.2f}',
                'recommendation': 'Implement automated payment reminders and credit policies'
            })
            
        # Billing errors
        if billing_errors_count > 0:
            error_rate = (billing_errors_count / total_invoices * 100) if total_invoices > 0 else 0
            leakage_points.append({
                'category': 'Billing',
                'severity': 'high' if error_rate > 5 else 'medium',
                'description': f'{billing_errors_count} billing errors detected',
                'impact': f'~${monthly_revenue * 0.02:.2f} estimated loss',
                'recommendation': 'Implement automated billing system' if not has_automated_billing else 'Review billing processes and add validation checks'
            })
            
        # Invoice gap
        if invoice_gap > 0:
            leakage_points.append({
                'category': 'Billing',
                'severity': 'high',
                'description': f'{invoice_gap} sales without invoices',
                'impact': f'~${invoice_gap * (monthly_revenue / total_sales):.2f}' if total_sales > 0 else 'Unknown',
                'recommendation': 'Ensure all sales are properly invoiced and tracked'
            })
            
        # Inventory shrinkage
        if inventory_shrinkage > 0:
            leakage_points.append({
                'category': 'Inventory',
                'severity': 'high' if inventory_shrinkage > monthly_revenue * 0.05 else 'medium',
                'description': 'Inventory shrinkage detected',
                'impact': f'${inventory_shrinkage:.2f}',
                'recommendation': 'Implement better inventory controls' if not tracks_inventory else 'Review security and handling procedures'
            })
            
        # Unrecorded sales
        if unrecorded_sales > 0:
            leakage_points.append({
                'category': 'Revenue Recognition',
                'severity': 'high',
                'description': 'Unrecorded sales',
                'impact': f'${unrecorded_sales:.2f}',
                'recommendation': 'Implement POS system integration and real-time recording'
            })
            
        # Pricing inconsistencies
        if pricing_inconsistencies > 0:
            leakage_points.append({
                'category': 'Pricing',
                'severity': 'medium',
                'description': f'{pricing_inconsistencies} pricing inconsistencies',
                'impact': f'~${monthly_revenue * 0.03:.2f} estimated loss',
                'recommendation': 'Standardize pricing and implement automated price management'
            })
            
        # Product performance
        if low_performing_products > total_products * 0.2:
            leakage_points.append({
                'category': 'Product Mix',
                'severity': 'medium',
                'description': f'{low_performing_products} low-performing products',
                'impact': 'Tied up inventory and resources',
                'recommendation': 'Review product portfolio and consider discontinuing underperformers'
            })
            
        # Generate AI-powered recovery strategies
        recovery_strategies = await self._generate_recovery_strategies(
            business_name, 
            industry, 
            business_model,
            leakage_points
        )
        
        # Risk assessment
        risk_level = self._calculate_risk_level(leakage_points)
        
        return {
            'analysis_id': f'EXIST_{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'business_name': business_name,
            'analysis_type': 'existing_business',
            'analysis_date': datetime.now().isoformat(),
            'data_period_months': data_period_months,
            'financial_summary': {
                'monthly_revenue': monthly_revenue,
                'total_loss': total_loss,
                'loss_percentage': (total_loss / monthly_revenue * 100) if monthly_revenue > 0 else 0,
                'refund_rate': refund_rate,
                'discount_rate': discount_rate
            },
            'operational_metrics': {
                'total_sales': total_sales,
                'total_invoices': total_invoices,
                'invoice_gap': invoice_gap,
                'billing_errors': billing_errors_count,
                'pricing_inconsistencies': pricing_inconsistencies
            },
            'leakage_breakdown': {
                'refunds': refunds_amount,
                'returns': returns_amount,
                'discounts': discounts_given,
                'uncollected': uncollected_payments,
                'inventory_shrinkage': inventory_shrinkage,
                'unrecorded_sales': unrecorded_sales
            },
            'leakage_points': leakage_points,
            'leakage_count': len(leakage_points),
            'total_identified_loss': total_loss,
            'risk_level': risk_level,
            'recovery_strategies': recovery_strategies,
            'executive_summary': f"{business_name} has {len(leakage_points)} active leakage points with total identified loss of ${total_loss:.2f} ({(total_loss/monthly_revenue*100):.1f}% of monthly revenue). Risk level: {risk_level}."
        }
        
    async def _generate_recovery_strategies(self, business_name: str, industry: str, 
                                           business_model: str, leakage_points: List[Dict]) -> List[Dict]:
        """
        Use AI to generate tailored recovery strategies based on identified leakage points
        """
        if not leakage_points:
            return []
            
        prompt = f"""
You are a revenue recovery expert. Analyze the following business and provide actionable recovery strategies.

Business: {business_name}
Industry: {industry}
Business Model: {business_model}

Identified Leakage Points:
{chr(10).join([f"- {point['category']}: {point['description']} (Impact: {point['impact']})" for point in leakage_points[:5]])}

Provide 3-5 specific, actionable recovery strategies. For each strategy:
1. Strategy name (short, clear title)
2. Description (2-3 sentences explaining the approach)
3. Expected impact (Low/Medium/High)
4. Implementation timeline (Short-term/Medium-term/Long-term)
5. Estimated recovery potential ($XXX or XX%)

Format as JSON array of strategy objects.
"""

        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a revenue recovery expert who provides specific, actionable strategies. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse JSON
            import json
            if content.startswith('```json'):
                content = content[7:-3].strip()
            elif content.startswith('```'):
                content = content[3:-3].strip()
                
            strategies = json.loads(content)
            return strategies if isinstance(strategies, list) else []
            
        except Exception as e:
            print(f"Error generating recovery strategies: {e}")
            # Fallback strategies
            return [
                {
                    'name': 'Process Automation',
                    'description': 'Implement automated systems to reduce manual errors and improve efficiency.',
                    'impact': 'High',
                    'timeline': 'Medium-term',
                    'estimated_recovery': '15-25% reduction in operational losses'
                },
                {
                    'name': 'Policy Review',
                    'description': 'Review and optimize pricing, discount, and refund policies.',
                    'impact': 'Medium',
                    'timeline': 'Short-term',
                    'estimated_recovery': '10-15% improvement in margins'
                }
            ]
    
    def _calculate_risk_level(self, leakage_points: List[Dict]) -> str:
        """
        Calculate overall risk level based on leakage points
        """
        if not leakage_points:
            return 'low'
            
        high_count = sum(1 for point in leakage_points if point['severity'] == 'high')
        medium_count = sum(1 for point in leakage_points if point['severity'] == 'medium')
        
        if high_count >= 3:
            return 'critical'
        elif high_count >= 1 or medium_count >= 3:
            return 'high'
        elif medium_count >= 1:
            return 'medium'
        else:
            return 'low'

# Singleton instance
business_analysis_service = BusinessAnalysisService()

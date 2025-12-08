"""
Enhanced Revenue Leakage Analysis Service
Intelligently analyzes ANY Excel/CSV format to detect financial issues
"""

import pandas as pd
import numpy as np
import uuid
from typing import Dict, List, Any


class EnhancedLeakageAnalyzer:
    """Advanced analyzer for detecting revenue leakages in uploaded data"""
    
    def __init__(self):
        # Comprehensive keyword dictionaries for intelligent column detection
        self.revenue_keywords = [
            'revenue', 'sales', 'income', 'amount', 'total', 'price', 'payment',
            'received', 'collection', 'receipt', 'billing', 'invoice', 'charge',
            'gross', 'net', 'proceeds', 'earning', 'turnover', 'value'
        ]
        
        self.cost_keywords = [
            'cost', 'expense', 'cogs', 'spend', 'payment', 'payable', 'expenditure',
            'overhead', 'outflow', 'disbursement', 'liability', 'purchase'
        ]
        
        self.discount_keywords = [
            'discount', 'rebate', 'reduction', 'markdown', 'allowance',
            'concession', 'offer', 'promo', 'coupon', 'voucher', 'deal'
        ]
        
        self.quantity_keywords = [
            'quantity', 'qty', 'units', 'count', 'number', 'volume', 'items',
            'pieces', 'orders', 'transactions', 'sold'
        ]
        
        self.date_keywords = [
            'date', 'time', 'day', 'month', 'year', 'period', 'timestamp',
            'created', 'modified', 'transaction', 'order_date', 'invoice_date'
        ]
        
        self.customer_keywords = [
            'customer', 'client', 'buyer', 'account', 'name', 'company',
            'organization', 'user', 'member', 'subscriber'
        ]
        
        self.product_keywords = [
            'product', 'item', 'sku', 'service', 'description', 'category',
            'type', 'model', 'variant', 'article'
        ]
        
        self.profit_keywords = [
            'profit', 'margin', 'markup', 'net_income', 'earnings', 'gain'
        ]
        
        self.refund_keywords = [
            'refund', 'return', 'chargeback', 'reversal', 'cancellation', 'void'
        ]
    
    def fuzzy_match_column(self, col_name: str, keywords: List[str]) -> bool:
        """Fuzzy match column names with keywords"""
        col_lower = str(col_name).lower().replace('_', ' ').replace('-', ' ')
        for keyword in keywords:
            if keyword in col_lower or col_lower in keyword:
                return True
        return False
    
    def detect_columns(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Intelligently detect column types"""
        all_columns = df.columns.tolist()
        
        return {
            'revenue': [col for col in all_columns if self.fuzzy_match_column(col, self.revenue_keywords)],
            'cost': [col for col in all_columns if self.fuzzy_match_column(col, self.cost_keywords)],
            'discount': [col for col in all_columns if self.fuzzy_match_column(col, self.discount_keywords)],
            'quantity': [col for col in all_columns if self.fuzzy_match_column(col, self.quantity_keywords)],
            'date': [col for col in all_columns if self.fuzzy_match_column(col, self.date_keywords)],
            'customer': [col for col in all_columns if self.fuzzy_match_column(col, self.customer_keywords)],
            'product': [col for col in all_columns if self.fuzzy_match_column(col, self.product_keywords)],
            'profit': [col for col in all_columns if self.fuzzy_match_column(col, self.profit_keywords)],
            'refund': [col for col in all_columns if self.fuzzy_match_column(col, self.refund_keywords)]
        }
    
    def analyze_negative_revenue(self, df: pd.DataFrame, revenue_cols: List[str]) -> List[Dict]:
        """Detect negative revenue transactions"""
        leakages = []
        
        for col in revenue_cols:
            try:
                if pd.api.types.is_numeric_dtype(df[col]):
                    negative_revenue = df[col] < 0
                    negative_count = negative_revenue.sum()
                    
                    if negative_count > 0:
                        negative_amount = abs(df[negative_revenue][col].sum())
                        affected_percentage = (negative_count / len(df) * 100)
                        
                        # Calculate additional impact (processing costs)
                        total_impact = negative_amount * 1.25  # 25% overhead
                        
                        severity = "critical" if affected_percentage > 10 else "high" if affected_percentage > 5 else "medium"
                        
                        leakages.append({
                            "id": str(uuid.uuid4())[:8],
                            "type": "Negative Revenue",
                            "column": col,
                            "description": f"Found {negative_count} transactions with negative revenue in '{col}' ({affected_percentage:.1f}% of all transactions). This indicates refunds, chargebacks, or data errors directly reducing revenue.",
                            "amount": float(total_impact),
                            "severity": severity,
                            "category": "Revenue Loss",
                            "status": "active",
                            "affected_rows": int(negative_count),
                            "recommendation": f"Investigate these {negative_count} transactions immediately. Analyze refund root causes or correct data errors. Implement validation rules to prevent future occurrences."
                        })
            except Exception as e:
                print(f"Error analyzing revenue column {col}: {e}")
        
        return leakages
    
    def analyze_excessive_discounts(self, df: pd.DataFrame, discount_cols: List[str], revenue_cols: List[str]) -> List[Dict]:
        """Analyze discount patterns"""
        leakages = []
        
        for col in discount_cols:
            try:
                if pd.api.types.is_numeric_dtype(df[col]):
                    total_discounts = abs(df[col].sum())
                    avg_discount = df[col].mean()
                    high_discount_count = (abs(df[col]) > abs(avg_discount) * 2).sum()
                    
                    discount_percentage = 0
                    if revenue_cols and total_discounts > 0:
                        first_rev_col = next((c for c in revenue_cols if c in df.columns and pd.api.types.is_numeric_dtype(df[c])), None)
                        if first_rev_col:
                            total_revenue = df[first_rev_col].sum()
                            if total_revenue > 0:
                                discount_percentage = (total_discounts / total_revenue * 100)
                    
                    if total_discounts > 0 and (discount_percentage > 15 or high_discount_count > len(df) * 0.1):
                        severity = "high" if discount_percentage > 20 else "medium"
                        
                        leakages.append({
                            "id": str(uuid.uuid4())[:8],
                            "type": "Excessive Discounts",
                            "column": col,
                            "description": f"Total discounts: ${total_discounts:,.2f}" + (f" ({discount_percentage:.1f}% of revenue)" if discount_percentage > 0 else "") + f". Found {high_discount_count} unusually high discounts. Excessive discounting erodes margins and trains customers to wait for sales.",
                            "amount": float(total_discounts),
                            "severity": severity,
                            "category": "Pricing Strategy",
                            "status": "active",
                            "affected_rows": int(high_discount_count),
                            "recommendation": f"Cap discounts at 15% maximum, require manager approval for >10%. Implement tiered pricing or bundle deals. Potential savings: ${total_discounts * 0.3:,.2f}"
                        })
            except Exception as e:
                print(f"Error analyzing discount column {col}: {e}")
        
        return leakages
    
    def analyze_missing_data(self, df: pd.DataFrame, revenue_cols: List[str], cost_cols: List[str]) -> List[Dict]:
        """Detect missing data in critical columns"""
        leakages = []
        
        critical_cols = revenue_cols + cost_cols
        
        for col in critical_cols:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                impact_amount = 0
                if col in revenue_cols and pd.api.types.is_numeric_dtype(df[col]):
                    avg_value = df[col].mean()
                    if not np.isnan(avg_value):
                        impact_amount = avg_value * null_count
                
                severity = "high" if col in revenue_cols else "medium" if col in cost_cols else "low"
                
                leakages.append({
                    "id": str(uuid.uuid4())[:8],
                    "type": "Missing Data",
                    "column": col,
                    "description": f"Found {null_count} missing values in '{col}' ({(null_count/len(df)*100):.1f}% of data). Missing financial data leads to incomplete analysis and potential revenue loss.",
                    "amount": float(impact_amount),
                    "severity": severity,
                    "category": "Data Quality",
                    "status": "active",
                    "affected_rows": int(null_count),
                    "recommendation": "Make critical fields mandatory in data entry systems. Implement real-time validation and staff training on data completeness."
                })
        
        return leakages
    
    def analyze_duplicates(self, df: pd.DataFrame, revenue_cols: List[str]) -> List[Dict]:
        """Detect duplicate transactions"""
        leakages = []
        
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            duplicate_amount = 0
            if revenue_cols:
                first_rev_col = next((c for c in revenue_cols if c in df.columns and pd.api.types.is_numeric_dtype(df[c])), None)
                if first_rev_col:
                    duplicate_rows = df[df.duplicated(keep=False)]
                    duplicate_amount = duplicate_rows[first_rev_col].sum() / 2
            
            leakages.append({
                "id": str(uuid.uuid4())[:8],
                "type": "Duplicate Transactions",
                "column": "All Columns",
                "description": f"Found {duplicate_count} duplicate rows - may indicate double billing, data entry errors, or system glitches.",
                "amount": float(abs(duplicate_amount)),
                "severity": "high",
                "category": "Data Quality",
                "status": "active",
                "affected_rows": int(duplicate_count),
                "recommendation": "Implement unique transaction IDs and duplicate detection in POS systems. Regular database deduplication and customer notification for duplicate charges."
            })
        
        return leakages
    
    def analyze_pricing_inconsistencies(self, df: pd.DataFrame, product_cols: List[str], revenue_cols: List[str]) -> List[Dict]:
        """Detect pricing inconsistencies across products"""
        leakages = []
        
        if product_cols and revenue_cols:
            for product_col in product_cols[:1]:
                for revenue_col in revenue_cols[:1]:
                    try:
                        if pd.api.types.is_numeric_dtype(df[revenue_col]):
                            price_by_product = df.groupby(product_col)[revenue_col].agg(['mean', 'std', 'count'])
                            price_by_product['cv'] = (price_by_product['std'] / price_by_product['mean'] * 100)
                            
                            inconsistent = price_by_product[
                                (price_by_product['cv'] > 20) &
                                (price_by_product['count'] > 2) &
                                (price_by_product['mean'] > 0)
                            ]
                            
                            if len(inconsistent) > 0:
                                estimated_loss = 0
                                for product, row in inconsistent.iterrows():
                                    optimal_price = row['mean'] + (row['std'] * 0.5)
                                    estimated_loss += (optimal_price - row['mean']) * row['count']
                                
                                leakages.append({
                                    "id": str(uuid.uuid4())[:8],
                                    "type": "Pricing Inconsistencies",
                                    "column": f"{product_col}, {revenue_col}",
                                    "description": f"Found {len(inconsistent)} products with inconsistent pricing (>20% price variation). Revenue leakage from underpricing some transactions.",
                                    "amount": float(max(estimated_loss, 0)),
                                    "severity": "medium",
                                    "category": "Pricing Strategy",
                                    "status": "active",
                                    "affected_rows": int(inconsistent['count'].sum()),
                                    "recommendation": "Standardize pricing across all channels. Create centralized price list and train sales staff on consistent pricing policies."
                                })
                    except Exception as e:
                        print(f"Error analyzing pricing consistency: {e}")
        
        return leakages
    
    def analyze_customer_concentration(self, df: pd.DataFrame, customer_cols: List[str], revenue_cols: List[str]) -> List[Dict]:
        """Analyze customer concentration risk"""
        leakages = []
        
        if customer_cols and revenue_cols:
            for customer_col in customer_cols[:1]:
                for revenue_col in revenue_cols[:1]:
                    try:
                        if pd.api.types.is_numeric_dtype(df[revenue_col]):
                            customer_revenue = df.groupby(customer_col)[revenue_col].sum().sort_values(ascending=False)
                            total_revenue = customer_revenue.sum()
                            
                            if len(customer_revenue) > 5:
                                top_customer_pct = (customer_revenue.iloc[0] / total_revenue * 100)
                                
                                if top_customer_pct > 30:
                                    risk_amount = customer_revenue.iloc[0] * 0.5
                                    
                                    leakages.append({
                                        "id": str(uuid.uuid4())[:8],
                                        "type": "Customer Concentration Risk",
                                        "column": f"{customer_col}, {revenue_col}",
                                        "description": f"Top customer represents {top_customer_pct:.1f}% of revenue (${customer_revenue.iloc[0]:,.2f}). Losing this customer would devastate the business.",
                                        "amount": float(risk_amount),
                                        "severity": "high",
                                        "category": "Business Risk",
                                        "status": "active",
                                        "affected_rows": len(df[df[customer_col] == customer_revenue.index[0]]),
                                        "recommendation": "Diversify customer base urgently. No single customer should exceed 20% of revenue. Develop new customer acquisition strategy."
                                    })
                    except Exception as e:
                        print(f"Error analyzing customer concentration: {e}")
        
        return leakages
    
    def analyze_complete(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform complete leakage analysis on uploaded data
        Returns comprehensive leakage report
        """
        # Detect all column types
        columns = self.detect_columns(df)
        
        # Run all analyses
        all_leakages = []
        
        all_leakages.extend(self.analyze_negative_revenue(df, columns['revenue']))
        all_leakages.extend(self.analyze_excessive_discounts(df, columns['discount'], columns['revenue']))
        all_leakages.extend(self.analyze_missing_data(df, columns['revenue'], columns['cost']))
        all_leakages.extend(self.analyze_duplicates(df, columns['revenue']))
        all_leakages.extend(self.analyze_pricing_inconsistencies(df, columns['product'], columns['revenue']))
        all_leakages.extend(self.analyze_customer_concentration(df, columns['customer'], columns['revenue']))
        
        # Calculate total financial impact
        total_amount = sum(l['amount'] for l in all_leakages)
        
        # Sort by amount (highest first)
        all_leakages.sort(key=lambda x: x['amount'], reverse=True)
        
        return {
            "total_leakages": len(all_leakages),
            "total_amount": total_amount,
            "items": all_leakages,
            "columns_analyzed": {
                "total_columns": len(df.columns),
                "revenue_columns": columns['revenue'],
                "cost_columns": columns['cost'],
                "discount_columns": columns['discount'],
                "quantity_columns": columns['quantity'],
                "customer_columns": columns['customer'],
                "product_columns": columns['product']
            }
        }

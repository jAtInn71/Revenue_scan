"""
Script to create sample Excel files for testing the Revenue Scan analysis system
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def create_sample_revenue_data():
    """Create a comprehensive sample revenue dataset"""
    
    # Generate dates for the last 3 months
    start_date = datetime.now() - timedelta(days=90)
    dates = [start_date + timedelta(days=i) for i in range(90)]
    
    # Sample data
    customers = ['ABC Corp', 'XYZ Inc', 'Acme Ltd', 'Tech Solutions', 'Global Services', 
                 'Best Buy Co', 'Premium Partners', 'Elite Enterprises', 'Smart Systems',
                 'Quality Products', 'Fast Delivery', 'Reliable Co', 'Innovation Hub',
                 'Digital Dynamics', 'Future Tech']
    
    products = ['Widget A', 'Widget B', 'Service Pack', 'Premium Plan', 'Basic Plan',
                'Product X', 'Product Y', 'Consulting', 'Support', 'Training',
                'Hardware', 'Software License', 'Maintenance', 'Installation']
    
    # Generate 300 transactions
    num_transactions = 300
    
    data = {
        'Transaction_Date': [random.choice(dates) for _ in range(num_transactions)],
        'Customer_Name': [random.choice(customers) for _ in range(num_transactions)],
        'Product_Name': [random.choice(products) for _ in range(num_transactions)],
        'Quantity': np.random.randint(1, 20, num_transactions),
        'Unit_Price': np.random.uniform(50, 500, num_transactions).round(2),
        'Total_Revenue': [],
        'Cost_of_Goods': [],
        'Discount_Amount': [],
        'Net_Amount': []
    }
    
    # Calculate derived fields
    for i in range(num_transactions):
        total_revenue = data['Quantity'][i] * data['Unit_Price'][i]
        
        # Add some discounts (15% of transactions)
        if random.random() < 0.15:
            discount = total_revenue * random.uniform(0.05, 0.25)
        else:
            discount = 0
        
        # Calculate cost (60-75% of revenue)
        cost = total_revenue * random.uniform(0.60, 0.75)
        
        net_amount = total_revenue - discount
        
        data['Total_Revenue'].append(round(total_revenue, 2))
        data['Cost_of_Goods'].append(round(cost, 2))
        data['Discount_Amount'].append(round(discount, 2))
        data['Net_Amount'].append(round(net_amount, 2))
    
    # Introduce some data quality issues for testing
    
    # 1. Add some negative revenues (refunds)
    refund_indices = random.sample(range(num_transactions), 8)
    for idx in refund_indices:
        data['Total_Revenue'][idx] = -abs(data['Total_Revenue'][idx])
        data['Net_Amount'][idx] = -abs(data['Net_Amount'][idx])
    
    # 2. Add missing data (10 rows)
    missing_indices = random.sample(range(num_transactions), 10)
    for idx in missing_indices:
        if random.random() < 0.5:
            data['Cost_of_Goods'][idx] = np.nan
        else:
            data['Discount_Amount'][idx] = np.nan
    
    # Create DataFrame first
    df = pd.DataFrame(data)
    
    # 3. Add duplicate rows (5 duplicates)
    duplicate_rows = []
    for _ in range(5):
        dup_idx = random.randint(0, num_transactions-1)
        duplicate_rows.append(df.iloc[dup_idx])
    
    if duplicate_rows:
        df = pd.concat([df, pd.DataFrame(duplicate_rows)], ignore_index=True)
    
    # 4. Add some pricing inconsistencies (same product, different prices)
    widget_a_indices = df[df['Product_Name'] == 'Widget A'].index.tolist()
    if len(widget_a_indices) > 5:
        # Make some Widget A transactions much cheaper
        for idx in widget_a_indices[:3]:
            df.loc[idx, 'Unit_Price'] = df.loc[idx, 'Unit_Price'] * 0.6
            df.loc[idx, 'Total_Revenue'] = df.loc[idx, 'Quantity'] * df.loc[idx, 'Unit_Price']
            df.loc[idx, 'Net_Amount'] = df.loc[idx, 'Total_Revenue'] - df.loc[idx, 'Discount_Amount']
    
    # Add additional computed columns
    df['Profit'] = df['Net_Amount'] - df['Cost_of_Goods']
    df['Profit_Margin_%'] = ((df['Profit'] / df['Net_Amount']) * 100).round(2)
    
    return df


def create_simple_sales_data():
    """Create a simpler sales dataset for basic testing"""
    
    data = {
        'Date': pd.date_range(start='2024-01-01', periods=50, freq='D'),
        'Sales_Amount': np.random.uniform(100, 1000, 50).round(2),
        'Cost': np.random.uniform(50, 500, 50).round(2),
        'Customer': [f'Customer_{i%10}' for i in range(50)],
        'Product': [f'Product_{chr(65+i%5)}' for i in range(50)]
    }
    
    df = pd.DataFrame(data)
    df['Profit'] = df['Sales_Amount'] - df['Cost']
    
    return df


def create_excel_with_multiple_sheets():
    """Create Excel file with multiple sheets"""
    
    # Create writer
    with pd.ExcelWriter('Sample_Revenue_Data.xlsx', engine='openpyxl') as writer:
        
        # Sheet 1: Complete Revenue Data
        df_complete = create_sample_revenue_data()
        df_complete.to_excel(writer, sheet_name='Revenue_Transactions', index=False)
        
        # Sheet 2: Simple Sales Data
        df_simple = create_simple_sales_data()
        df_simple.to_excel(writer, sheet_name='Daily_Sales', index=False)
        
        # Sheet 3: Summary Statistics
        summary = pd.DataFrame({
            'Metric': ['Total Revenue', 'Total Cost', 'Net Profit', 'Transactions', 'Avg Transaction'],
            'Value': [
                df_complete['Total_Revenue'].sum(),
                df_complete['Cost_of_Goods'].sum(),
                df_complete['Profit'].sum(),
                len(df_complete),
                df_complete['Total_Revenue'].mean()
            ]
        })
        summary.to_excel(writer, sheet_name='Summary', index=False)
    
    print("✅ Created 'Sample_Revenue_Data.xlsx' with 3 sheets")


def create_csv_sample():
    """Create CSV sample file"""
    df = create_sample_revenue_data()
    df.to_csv('Sample_Revenue_Data.csv', index=False)
    print("✅ Created 'Sample_Revenue_Data.csv'")


def create_problem_dataset():
    """Create a dataset with multiple issues for testing detection"""
    
    data = {
        'Invoice_Date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
        'Customer_ID': [f'CUST_{i%15:03d}' for i in range(100)],
        'Product_Code': [f'SKU_{i%8:03d}' for i in range(100)],
        'Revenue': np.random.uniform(100, 2000, 100).round(2),
        'Cost': np.random.uniform(50, 1500, 100).round(2),
        'Discount': np.random.uniform(0, 200, 100).round(2)
    }
    
    df = pd.DataFrame(data)
    
    # Introduce various problems
    
    # 1. Excessive discounts (25% of revenue for some)
    df.loc[10:15, 'Discount'] = df.loc[10:15, 'Revenue'] * 0.25
    
    # 2. Negative revenue (refunds)
    df.loc[20:25, 'Revenue'] = -abs(df.loc[20:25, 'Revenue'])
    
    # 3. Missing data
    df.loc[30:35, 'Cost'] = np.nan
    df.loc[40:42, 'Revenue'] = np.nan
    
    # 4. Duplicates
    df = pd.concat([df, df.iloc[50:55]], ignore_index=True)
    
    # 5. Customer concentration (one customer has 40% of revenue)
    df.loc[60:80, 'Customer_ID'] = 'CUST_999'
    df.loc[60:80, 'Revenue'] = np.random.uniform(1000, 5000, 21)
    
    # 6. Pricing inconsistencies (same SKU, very different prices)
    sku_001_indices = df[df['Product_Code'] == 'SKU_001'].index
    if len(sku_001_indices) > 3:
        df.loc[sku_001_indices[0], 'Revenue'] = 500
        df.loc[sku_001_indices[1], 'Revenue'] = 1500  # 3x difference
        df.loc[sku_001_indices[2], 'Revenue'] = 800
    
    df.to_excel('Problem_Dataset.xlsx', index=False)
    print("✅ Created 'Problem_Dataset.xlsx' (contains intentional issues for testing)")


if __name__ == '__main__':
    print("🎯 Creating sample Excel and CSV files for Revenue Scan testing...\n")
    
    create_excel_with_multiple_sheets()
    create_csv_sample()
    create_problem_dataset()
    
    print("\n✨ All sample files created successfully!")
    print("\n📋 Files created:")
    print("  1. Sample_Revenue_Data.xlsx - Complete dataset with 3 sheets")
    print("  2. Sample_Revenue_Data.csv - CSV version")
    print("  3. Problem_Dataset.xlsx - Dataset with intentional issues")
    print("\n🚀 Upload these files to test the Revenue Scan analysis system!")

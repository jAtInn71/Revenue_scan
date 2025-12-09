"""
Test script for Business Analysis endpoints
Run this to verify the backend is working correctly
"""

import asyncio
import sys
sys.path.append('backend')

from services.business_analysis_service import business_analysis_service

async def test_new_business_analysis():
    """Test new business analysis"""
    print("\n" + "="*60)
    print("Testing NEW BUSINESS ANALYSIS")
    print("="*60)
    
    test_data = {
        'business_name': 'TechGadgets Store',
        'industry': 'Electronics',
        'business_model': 'ecommerce',
        'pricing_strategy': 'competitive',
        'expected_monthly_revenue': 50000,
        'product_price': 99.99,
        'product_cost_per_unit': 40.00,
        'expected_units_sold': 500,
        'fixed_monthly_costs': 10000,
        'planned_discount_percentage': 10,
        'expected_refund_rate': 5,
        'payment_methods': ['card', 'digital_wallet'],
        'inventory_tracking': True,
        'has_billing_system': False
    }
    
    try:
        result = await business_analysis_service.analyze_new_business(test_data)
        
        print(f"\n✅ Analysis ID: {result['analysis_id']}")
        print(f"✅ Business: {result['business_name']}")
        print(f"✅ Risk Level: {result['risk_level'].upper()}")
        print(f"✅ Leakage Points Found: {result['leakage_count']}")
        print(f"✅ Total Potential Loss: ${result['total_potential_loss']:.2f}")
        
        print(f"\n📊 Financial Summary:")
        fs = result['financial_summary']
        print(f"   Expected Revenue: ${fs['expected_monthly_revenue']:,.2f}")
        print(f"   Net Revenue: ${fs['net_revenue']:,.2f}")
        print(f"   Profit Margin: {fs['profit_margin']:.1f}%")
        
        print(f"\n⚠️  Leakage Points:")
        for i, point in enumerate(result['leakage_points'][:3], 1):
            print(f"   {i}. [{point['severity'].upper()}] {point['category']}")
            print(f"      {point['description']}")
            print(f"      Impact: {point['impact']}")
        
        print(f"\n💡 Recovery Strategies: {len(result['recovery_strategies'])} strategies generated")
        for i, strategy in enumerate(result['recovery_strategies'][:2], 1):
            print(f"   {i}. {strategy['name']}")
            print(f"      Timeline: {strategy['timeline']}")
        
        print(f"\n📝 Executive Summary:")
        print(f"   {result['executive_summary']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_existing_business_analysis():
    """Test existing business analysis"""
    print("\n" + "="*60)
    print("Testing EXISTING BUSINESS ANALYSIS")
    print("="*60)
    
    test_data = {
        'business_name': 'Fashion Boutique',
        'industry': 'Fashion',
        'business_model': 'retail',
        'monthly_revenue': 100000,
        'total_sales': 500,
        'total_invoices': 480,
        'total_products': 150,
        'refunds_amount': 5000,
        'returns_amount': 3000,
        'discounts_given': 12000,
        'uncollected_payments': 2000,
        'inventory_shrinkage': 4000,
        'unrecorded_sales': 1500,
        'billing_errors_count': 15,
        'pricing_inconsistencies': 8,
        'low_performing_products': 20,
        'high_cost_products': 10,
        'has_automated_billing': False,
        'tracks_inventory': True,
        'uses_crm': False,
        'payment_methods': ['cash', 'card'],
        'data_period_months': 3
    }
    
    try:
        result = await business_analysis_service.analyze_existing_business(test_data)
        
        print(f"\n✅ Analysis ID: {result['analysis_id']}")
        print(f"✅ Business: {result['business_name']}")
        print(f"✅ Risk Level: {result['risk_level'].upper()}")
        print(f"✅ Leakage Points Found: {result['leakage_count']}")
        print(f"✅ Total Identified Loss: ${result['total_identified_loss']:,.2f}")
        
        print(f"\n📊 Financial Summary:")
        fs = result['financial_summary']
        print(f"   Monthly Revenue: ${fs['monthly_revenue']:,.2f}")
        print(f"   Total Loss: ${fs['total_loss']:,.2f}")
        print(f"   Loss Percentage: {fs['loss_percentage']:.1f}%")
        
        print(f"\n💸 Loss Breakdown:")
        lb = result['leakage_breakdown']
        print(f"   Refunds: ${lb['refunds']:,.2f}")
        print(f"   Returns: ${lb['returns']:,.2f}")
        print(f"   Discounts: ${lb['discounts']:,.2f}")
        print(f"   Uncollected: ${lb['uncollected']:,.2f}")
        print(f"   Inventory Shrinkage: ${lb['inventory_shrinkage']:,.2f}")
        print(f"   Unrecorded Sales: ${lb['unrecorded_sales']:,.2f}")
        
        print(f"\n⚠️  Leakage Points:")
        for i, point in enumerate(result['leakage_points'][:3], 1):
            print(f"   {i}. [{point['severity'].upper()}] {point['category']}")
            print(f"      {point['description']}")
            print(f"      Impact: {point['impact']}")
        
        print(f"\n💡 Recovery Strategies: {len(result['recovery_strategies'])} strategies generated")
        for i, strategy in enumerate(result['recovery_strategies'][:2], 1):
            print(f"   {i}. {strategy['name']}")
            print(f"      Timeline: {strategy['timeline']}")
        
        print(f"\n📝 Executive Summary:")
        print(f"   {result['executive_summary']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("BUSINESS ANALYSIS SERVICE TEST")
    print("="*60)
    print("\nThis will test both analysis endpoints with sample data.")
    print("OpenAI API will be called to generate intelligent insights.\n")
    
    # Test 1: New Business
    test1_passed = await test_new_business_analysis()
    
    # Test 2: Existing Business
    test2_passed = await test_existing_business_analysis()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"New Business Analysis: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Existing Business Analysis: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Backend is ready to use.")
        print("\nNext steps:")
        print("1. Start the backend: cd backend && python -m uvicorn main:app --reload")
        print("2. Start the frontend: cd frontend && npm run dev")
        print("3. Test in browser at http://localhost:5173")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("\nCommon issues:")
        print("- Missing OPENAI_API_KEY in .env file")
        print("- Invalid OpenAI API key")
        print("- Network connectivity issues")


if __name__ == "__main__":
    asyncio.run(main())

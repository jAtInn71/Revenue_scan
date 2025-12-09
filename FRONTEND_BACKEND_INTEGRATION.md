# Frontend-Backend Integration Guide

## Business Analysis Features

This document explains how the **New Business Analysis** and **Existing Business Analysis** features work together between the frontend and backend.

---

## 🎯 Overview

### What's Already Done
✅ Frontend forms for New Business and Existing Business analysis  
✅ Backend API endpoints at `/api/business/new/analyze` and `/api/business/existing/analyze`  
✅ OpenAI integration for intelligent analysis  
✅ Database storage for analysis history  
✅ API client functions in `frontend/src/services/api.js`

### What You Need to Do
1. Add your OpenAI API key to backend `.env` file
2. Start the backend server
3. Start the frontend development server
4. Test the analysis features

---

## 🚀 Quick Start

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create .env file from example
copy .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-key-here

# Start the backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Frontend Setup

```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev
```

### Step 3: Test the Features

Open your browser to `http://localhost:5173` and navigate to:
- **New Business Analysis**: `/new-business-analyze`
- **Existing Business Analysis**: `/existing-business-analyze`

---

## 📋 API Integration Details

### New Business Analysis

**Frontend Component**: `frontend/src/pages/NewBusinessAnalyze.jsx`

**API Call**:
```javascript
import { analyzeNewBusiness } from '../services/api'

const response = await analyzeNewBusiness({
  business_name: "TechGadgets Store",
  industry: "Electronics",
  business_model: "ecommerce",
  pricing_strategy: "competitive",
  expected_monthly_revenue: 50000,
  product_price: 99.99,
  product_cost_per_unit: 40.00,
  expected_units_sold: 500,
  fixed_monthly_costs: 10000,
  planned_discount_percentage: 10,
  expected_refund_rate: 5,
  payment_methods: ["card", "digital_wallet"],
  inventory_tracking: true,
  has_billing_system: false
})
```

**Backend Endpoint**: `POST /api/business/new/analyze`

**Response Structure**:
```json
{
  "success": true,
  "analysis": {
    "analysis_id": "NEW_20251209120000",
    "business_name": "TechGadgets Store",
    "analysis_type": "new_business",
    "analysis_date": "2025-12-09T12:00:00",
    "financial_summary": {
      "expected_monthly_revenue": 50000,
      "gross_revenue": 49999.50,
      "total_costs": 30000,
      "discount_loss": 4999.95,
      "refund_loss": 2499.98,
      "net_revenue": 17499.57,
      "profit_margin": 35.0
    },
    "leakage_points": [
      {
        "category": "Billing",
        "severity": "high",
        "description": "No automated billing system",
        "impact": "~15 potential billing errors/month",
        "recommendation": "Implement automated billing software to reduce human errors"
      }
    ],
    "leakage_count": 3,
    "total_potential_loss": 7499.93,
    "risk_level": "medium",
    "recovery_strategies": [
      {
        "name": "Automated Billing Implementation",
        "description": "Deploy a cloud-based billing system to eliminate manual errors...",
        "impact": "High",
        "timeline": "Medium-term",
        "estimated_recovery": "15-20% reduction in billing errors"
      }
    ],
    "executive_summary": "TechGadgets Store shows medium risk with 3 potential leakage points identified..."
  }
}
```

---

### Existing Business Analysis

**Frontend Component**: `frontend/src/pages/ExistingBusinessAnalyze.jsx`

**API Call**:
```javascript
import { analyzeExistingBusiness } from '../services/api'

const response = await analyzeExistingBusiness({
  business_name: "Fashion Boutique",
  industry: "Fashion",
  business_model: "retail",
  monthly_revenue: 100000,
  total_sales: 500,
  total_invoices: 480,
  total_products: 150,
  refunds_amount: 5000,
  returns_amount: 3000,
  discounts_given: 12000,
  uncollected_payments: 2000,
  inventory_shrinkage: 4000,
  unrecorded_sales: 1500,
  billing_errors_count: 15,
  pricing_inconsistencies: 8,
  low_performing_products: 20,
  high_cost_products: 10,
  has_automated_billing: false,
  tracks_inventory: true,
  uses_crm: false,
  payment_methods: ["cash", "card"],
  data_period_months: 3
})
```

**Backend Endpoint**: `POST /api/business/existing/analyze`

**Response Structure**:
```json
{
  "success": true,
  "analysis": {
    "analysis_id": "EXIST_20251209120000",
    "business_name": "Fashion Boutique",
    "analysis_type": "existing_business",
    "analysis_date": "2025-12-09T12:00:00",
    "data_period_months": 3,
    "financial_summary": {
      "monthly_revenue": 100000,
      "total_loss": 27500,
      "loss_percentage": 27.5,
      "refund_rate": 5.0,
      "discount_rate": 12.0
    },
    "operational_metrics": {
      "total_sales": 500,
      "total_invoices": 480,
      "invoice_gap": 20,
      "billing_errors": 15,
      "pricing_inconsistencies": 8
    },
    "leakage_breakdown": {
      "refunds": 5000,
      "returns": 3000,
      "discounts": 12000,
      "uncollected": 2000,
      "inventory_shrinkage": 4000,
      "unrecorded_sales": 1500
    },
    "leakage_points": [
      {
        "category": "Discounts",
        "severity": "medium",
        "description": "Excessive discounts (12.0%)",
        "impact": "$12000.00",
        "recommendation": "Implement strategic discount policies and reduce blanket discounts"
      }
    ],
    "leakage_count": 6,
    "total_identified_loss": 27500,
    "risk_level": "high",
    "recovery_strategies": [
      {
        "name": "Discount Policy Optimization",
        "description": "Implement data-driven discount strategies...",
        "impact": "High",
        "timeline": "Short-term",
        "estimated_recovery": "20-30% reduction in discount losses"
      }
    ],
    "executive_summary": "Fashion Boutique has 6 active leakage points with total identified loss of $27500.00 (27.5% of monthly revenue)..."
  }
}
```

---

## 🔧 How It Works

### Data Flow

```
┌─────────────────┐
│  User fills     │
│  form in React  │
│  component      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Form submits   │
│  via onSubmit   │
│  handler        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  API function   │
│  from api.js    │
│  makes POST     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI routes │
│  receive data   │
│  (/business/*)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Business       │
│  Analysis       │
│  Service        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OpenAI API     │
│  generates      │
│  insights       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Response sent  │
│  back to React  │
│  component      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Results        │
│  displayed to   │
│  user           │
└─────────────────┘
```

### OpenAI Integration

The backend uses OpenAI's GPT-4o-mini model to:

1. **Analyze Business Context**: Understands your industry, business model, and operational data
2. **Generate Recovery Strategies**: Creates tailored, actionable recommendations
3. **Provide Executive Summaries**: Summarizes findings in business language
4. **Calculate Risk Levels**: Assesses severity of identified issues

**File**: `backend/services/business_analysis_service.py`

Key function: `_generate_recovery_strategies()`

```python
async def _generate_recovery_strategies(self, business_name, industry, 
                                       business_model, leakage_points):
    prompt = f"""
    You are a revenue recovery expert. Analyze the following business 
    and provide actionable recovery strategies.
    
    Business: {business_name}
    Industry: {industry}
    Business Model: {business_model}
    
    Identified Leakage Points:
    {leakage_points}
    
    Provide 3-5 specific, actionable recovery strategies...
    """
    
    response = await self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[...],
        temperature=0.7
    )
    
    return strategies
```

---

## 🧪 Testing

### Manual Testing

1. **Test New Business Analysis**:
   - Go to http://localhost:5173/new-business-analyze
   - Fill out the form with realistic data
   - Click "Analyze Business"
   - Wait 2-5 seconds
   - Verify you see:
     - Financial summary
     - Risk level
     - Leakage points
     - Recovery strategies
     - Executive summary

2. **Test Existing Business Analysis**:
   - Go to http://localhost:5173/existing-business-analyze
   - Fill out the form with operational metrics
   - Click "Analyze Business"
   - Wait 2-5 seconds
   - Verify you see:
     - Financial summary
     - Loss breakdown
     - Identified issues
     - Recovery strategies

### Automated Testing

Run the test script:

```bash
python test_business_analysis.py
```

This will test both endpoints with sample data and display results.

---

## 🔍 Troubleshooting

### Issue: "Failed to analyze business"

**Possible Causes**:
1. Backend not running
2. Invalid OpenAI API key
3. Network connectivity issues

**Solutions**:
```bash
# Check backend is running
curl http://localhost:8000/health

# Verify .env file exists and has correct key
cat backend/.env | grep OPENAI_API_KEY

# Check backend logs for errors
# (Look in terminal where backend is running)
```

### Issue: "CORS Error"

**Solution**: Backend is configured to allow all origins. Ensure:
- Backend is running on port 8000
- Frontend is making requests to http://localhost:8000/api/business/*

### Issue: Analysis takes too long

**Expected Behavior**: OpenAI API calls take 2-5 seconds. The frontend shows a loading state with "Analyzing..." button.

**If it takes longer**:
- Check your internet connection
- Verify OpenAI API status: https://status.openai.com/
- Check backend logs for errors

### Issue: Results not displaying

**Check**:
1. Browser console for errors (F12)
2. Network tab to see API response
3. Backend terminal for errors
4. Response structure matches expected format

---

## 📊 Understanding the Results

### Risk Levels

- **Low**: 0-2 minor issues, minimal revenue impact
- **Medium**: 2-4 issues, moderate revenue impact (5-15%)
- **High**: 4+ issues, significant revenue impact (15-25%)
- **Critical**: 5+ high-severity issues, major revenue impact (25%+)

### Severity Ratings

- **High**: Immediate attention required, significant revenue impact
- **Medium**: Important but not urgent, moderate impact
- **Low**: Nice to address, minimal impact

### Recovery Strategies

Each strategy includes:
- **Name**: Clear, actionable title
- **Description**: What to do and why
- **Impact**: Expected revenue recovery (Low/Medium/High)
- **Timeline**: When to implement (Short/Medium/Long-term)
- **Estimated Recovery**: Specific revenue or percentage improvement

---

## 💰 OpenAI API Costs

- **Model**: gpt-4o-mini (cost-effective)
- **Cost per analysis**: ~$0.001-0.003
- **1000 analyses**: ~$1-3
- **Monthly budget**: Set usage limits in OpenAI dashboard

---

## 🔐 Security Best Practices

1. **Never commit .env file**: Listed in .gitignore
2. **Use environment variables**: Already configured
3. **Rotate API keys**: Change periodically
4. **Monitor usage**: Check OpenAI dashboard
5. **Set rate limits**: Prevent abuse in production

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/api/docs
- **OpenAI API**: https://platform.openai.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Hook Form**: https://react-hook-form.com/

---

## ✅ Checklist

Before going live, ensure:

- [ ] OpenAI API key configured in .env
- [ ] Backend starts without errors
- [ ] Frontend connects to backend
- [ ] New Business Analysis works end-to-end
- [ ] Existing Business Analysis works end-to-end
- [ ] Results display correctly
- [ ] Error handling works (try invalid data)
- [ ] Loading states show properly
- [ ] Analysis history is saved (check database)

---

## 🎉 You're All Set!

Your Business Analysis features are now fully integrated with OpenAI-powered intelligent analysis. Users can:

1. **New Business**: Get risk assessment before launch
2. **Existing Business**: Identify and recover revenue leaks
3. **AI Insights**: Receive tailored recovery strategies
4. **Track History**: Review past analyses

**Happy analyzing! 🚀**

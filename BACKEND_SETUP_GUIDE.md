# Backend Setup Guide for Business Analysis

## Overview
This guide helps you connect the frontend Business Analysis pages (New Business and Existing Business) with the backend API that uses OpenAI for intelligent analysis.

## Prerequisites
- Python 3.8+
- OpenAI API Key
- Backend dependencies installed

## Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Configure OpenAI API Key

Create a `.env` file in the `backend` directory:

```bash
# Copy the example file
copy .env.example .env
```

Edit the `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
SECRET_KEY=your-secret-key-at-least-32-characters-long
```

## Step 3: API Endpoints

The backend provides the following endpoints:

### New Business Analysis
- **Endpoint**: `POST /api/business/new/analyze`
- **Purpose**: Analyze a new business for potential revenue leakage risks
- **Request Body**: NewBusinessForm (see frontend form)
- **Response**: Analysis with risk assessment and recommendations

### Existing Business Analysis
- **Endpoint**: `POST /api/business/existing/analyze`
- **Purpose**: Analyze existing business operations for revenue leaks
- **Request Body**: ExistingBusinessForm (see frontend form)
- **Response**: Analysis with identified leaks and recovery strategies

### Get Analysis History
- **Endpoint**: `GET /api/business/history?limit=10`
- **Purpose**: Retrieve previous analyses
- **Response**: List of saved analyses

### Get Specific Analysis
- **Endpoint**: `GET /api/business/analysis/{analysis_id}`
- **Purpose**: Retrieve a specific analysis by ID
- **Response**: Full analysis details

## Step 4: Start the Backend

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or use the batch file:
```bash
START_BACKEND.bat
```

## Step 5: Verify Backend is Running

Open your browser and navigate to:
- API Documentation: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/health

## Step 6: Start the Frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

## How It Works

### New Business Analysis Flow
1. User fills out the form in the frontend (`NewBusinessAnalyze.jsx`)
2. Frontend calls `analyzeNewBusiness(formData)` from `api.js`
3. Backend receives request at `/api/business/new/analyze`
4. Backend processes data and calls OpenAI for intelligent analysis
5. OpenAI generates:
   - Risk assessment
   - Potential leakage points
   - Recovery strategies
   - Executive summary
6. Response is returned to frontend and displayed

### Existing Business Analysis Flow
1. User fills out the form in the frontend (`ExistingBusinessAnalyze.jsx`)
2. Frontend calls `analyzeExistingBusiness(formData)` from `api.js`
3. Backend receives request at `/api/business/existing/analyze`
4. Backend calculates actual revenue loss from provided data
5. OpenAI analyzes patterns and generates:
   - Identified leakage points
   - Recovery strategies
   - Priority recommendations
6. Response is returned to frontend and displayed

## Features Powered by OpenAI

### 1. **Intelligent Risk Assessment**
   - Analyzes business model and industry
   - Identifies high-risk areas
   - Provides severity ratings

### 2. **Custom Recovery Strategies**
   - Tailored to your business type
   - Industry-specific recommendations
   - Implementation timelines
   - Expected recovery amounts

### 3. **Executive Summaries**
   - Concise overview of findings
   - Key metrics highlighted
   - Action items prioritized

### 4. **Smart Recommendations**
   - Context-aware suggestions
   - Best practices from industry
   - Technology suggestions
   - Process improvements

## Response Format

### New Business Analysis Response
```json
{
  "success": true,
  "analysis": {
    "analysis_id": "NEW_20251209120000",
    "business_name": "TechGadgets Store",
    "analysis_type": "new_business",
    "financial_summary": {
      "expected_monthly_revenue": 50000,
      "gross_revenue": 50000,
      "total_costs": 30000,
      "net_revenue": 17500,
      "profit_margin": 35
    },
    "leakage_points": [
      {
        "category": "Billing",
        "severity": "high",
        "description": "No automated billing system",
        "impact": "~30 potential billing errors/month",
        "recommendation": "Implement automated billing software"
      }
    ],
    "leakage_count": 3,
    "total_potential_loss": 2500,
    "risk_level": "medium",
    "recovery_strategies": [
      {
        "name": "Automated Billing Implementation",
        "description": "Deploy cloud-based billing system...",
        "impact": "High",
        "timeline": "Medium-term",
        "estimated_recovery": "15-20% reduction in billing errors"
      }
    ],
    "executive_summary": "TechGadgets Store shows medium risk..."
  }
}
```

### Existing Business Analysis Response
```json
{
  "success": true,
  "analysis": {
    "analysis_id": "EXIST_20251209120000",
    "business_name": "Fashion Boutique",
    "analysis_type": "existing_business",
    "financial_summary": {
      "monthly_revenue": 100000,
      "total_loss": 27500,
      "loss_percentage": 27.5,
      "refund_rate": 5,
      "discount_rate": 12
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
        "recommendation": "Implement strategic discount policies"
      }
    ],
    "leakage_count": 6,
    "total_identified_loss": 27500,
    "risk_level": "high",
    "recovery_strategies": [...],
    "executive_summary": "Fashion Boutique has 6 active leakage points..."
  }
}
```

## Troubleshooting

### Issue: OpenAI API Key Error
**Solution**: Ensure your `.env` file has a valid OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

### Issue: CORS Error
**Solution**: Backend is configured to allow all origins in development. Ensure backend is running on port 8000.

### Issue: Analysis Taking Too Long
**Solution**: OpenAI API calls may take 2-5 seconds. This is normal. The frontend shows a loading state.

### Issue: Backend Not Starting
**Solution**: 
1. Check if port 8000 is available
2. Verify Python dependencies are installed
3. Check for syntax errors in code

## Testing the Integration

### Test New Business Analysis
1. Navigate to http://localhost:5173/new-business-analyze
2. Fill out the form with sample data
3. Click "Analyze Business"
4. Wait 2-5 seconds for AI analysis
5. Review the comprehensive results

### Test Existing Business Analysis
1. Navigate to http://localhost:5173/existing-business-analyze
2. Fill out the form with operational data
3. Click "Analyze Business"
4. Wait 2-5 seconds for AI analysis
5. Review identified leakage points and recovery strategies

## Security Notes

1. **Never commit `.env` file** - Keep your API keys secret
2. **Use environment variables** - Don't hardcode sensitive data
3. **Rotate API keys regularly** - Change keys periodically
4. **Monitor API usage** - Check OpenAI dashboard for usage

## Cost Considerations

- Each analysis makes 1-2 OpenAI API calls
- Using `gpt-4o-mini` model (cost-effective)
- Average cost per analysis: ~$0.001-0.003
- 1000 analyses ≈ $1-3

## Next Steps

1. Get your OpenAI API key from https://platform.openai.com/api-keys
2. Configure the `.env` file
3. Start the backend
4. Start the frontend
5. Test both analysis features
6. Review the AI-generated insights

## Support

For issues or questions:
- Check the API documentation at `/api/docs`
- Review error logs in the backend terminal
- Ensure all dependencies are installed
- Verify OpenAI API key is valid

# Smart Revenue Leakage Advisor

AI-Powered System to Prevent and Recover Lost Revenue for Businesses

## 🚀 Features

- **Dual Analysis Mode**: Support for both new and existing businesses
- **AI-Powered Insights**: Intelligent recommendations using OpenAI GPT
- **Revenue Leakage Detection**: Identifies 7+ types of revenue leaks
- **Risk Assessment**: Comprehensive risk scoring (0-100)
- **Recovery Strategy**: Actionable recovery plans with timelines
- **PDF Reports**: Professional reports with charts and recommendations
- **RESTful API**: Clean, well-documented API endpoints
- **Real-time Analytics**: Dashboard with KPIs and metrics

## 📋 System Requirements

- Python 3.9+
- Node.js 16+ (for frontend)
- 2GB RAM minimum
- 500MB disk space

## 🛠️ Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key (optional)
```

### 3. Run the Server

```bash
python main.py
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/api/docs`

## 📡 API Endpoints

### Business Analysis

**POST** `/api/business/new/analyze`
- Analyze a new business for potential risks
- Returns: Revenue analysis, risk assessment, recovery strategy

**POST** `/api/business/existing/analyze`
- Analyze existing business for revenue leakage
- Returns: Detected leaks, recovery recommendations

**GET** `/api/business/analysis/{analysis_id}`
- Retrieve a specific analysis

**GET** `/api/business/analyses`
- List all analyses with pagination

### Analytics

**GET** `/api/analysis/metrics/{analysis_id}`
- Get key metrics and KPIs

**GET** `/api/analysis/compare?analysis_ids=id1,id2`
- Compare multiple analyses

**GET** `/api/analysis/statistics`
- Platform-wide statistics

### Reports

**POST** `/api/reports/generate`
- Generate PDF report

**GET** `/api/reports/download/{report_id}`
- Download generated report

## 📊 Analysis Types

### For New Businesses
- Pricing strategy risks
- Cost structure analysis
- Discount planning evaluation
- Payment method risks
- Operational setup assessment
- Inventory management risks
- Expected refund rate analysis

### For Existing Businesses
- Refunds and returns analysis
- Discount mismanagement detection
- Billing error identification
- Pricing inconsistencies
- Inventory shrinkage
- Uncollected payments
- Unrecorded sales
- Product performance analysis

## 🔑 Key Metrics

- **Revenue Leakage Percentage**: % of revenue lost
- **Risk Score**: 0-100 scale
- **Recoverable Amount**: Potential recovery
- **Leakage Points**: Specific issues identified
- **Severity Levels**: Critical, High, Medium, Low

## 🎯 Use Cases

1. **Startup Launch**: Prevent revenue leaks before they happen
2. **Business Audit**: Identify current revenue losses
3. **Investor Pitch**: Show revenue protection measures
4. **Financial Planning**: Optimize revenue streams
5. **Operational Review**: Improve business processes

## 📱 Frontend (Coming Soon)

React-based dashboard with:
- Interactive forms
- Real-time analysis
- Data visualization
- Report download
- Comparison tools

## 🧪 Testing

```bash
pytest
```

## 📖 Documentation

- API Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - See LICENSE file

## 👥 Authors

Built by Expert Developers

## 🌟 Demo

Perfect for:
- Technical events
- Business exhibitions
- Startup competitions
- Investor demos

---

**Smart Revenue Leakage Advisor** - Protect Your Revenue, Grow Your Business 📈

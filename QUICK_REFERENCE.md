# Quick Reference - Business Analysis Backend

## ⚡ Quick Start (3 Steps)

```bash
# 1. Add OpenAI key to backend/.env
OPENAI_API_KEY=sk-your-key-here

# 2. Start servers
START_ANALYSIS.bat

# 3. Open browser
http://localhost:5173
```

---

## 📍 Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/business/new/analyze` | Analyze new business |
| POST | `/api/business/existing/analyze` | Analyze existing business |
| GET | `/api/business/analysis/{id}` | Get specific analysis |
| GET | `/api/business/history` | Get analysis history |

---

## 🔧 Configuration

**Required:**
- `backend/.env` → Add `OPENAI_API_KEY=sk-...`

**Optional:**
- Risk thresholds in `.env`
- Database path
- CORS origins

---

## 🧪 Testing

```bash
# Test backend only
python test_business_analysis.py

# Test via browser
http://localhost:5173/new-business-analyze
http://localhost:5173/existing-business-analyze

# Check API docs
http://localhost:8000/api/docs
```

---

## 📊 Response Format

```json
{
  "success": true,
  "analysis": {
    "analysis_id": "...",
    "business_name": "...",
    "financial_summary": {},
    "leakage_points": [],
    "recovery_strategies": [],
    "risk_level": "medium",
    "executive_summary": "..."
  }
}
```

---

## 💰 Costs

- Per analysis: $0.001-0.003
- 1000 analyses: ~$1-3
- Model: gpt-4o-mini (fast & cheap)

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| OpenAI Error | Add valid API key to `.env` |
| Network Error | Start backend on port 8000 |
| Slow response | Normal! OpenAI takes 2-5 sec |
| Backend won't start | `pip install -r requirements.txt` |

---

## 📁 Key Files

```
backend/
├─ .env                           ← API keys HERE
├─ api/routes/business_routes.py  ← Endpoints
└─ services/business_analysis_service.py ← Logic

frontend/
├─ src/pages/NewBusinessAnalyze.jsx
├─ src/pages/ExistingBusinessAnalyze.jsx
└─ src/services/api.js            ← API calls
```

---

## 🎯 What Gets Analyzed

### New Business
- Business model & industry
- Pricing strategy
- Expected revenue/costs
- Systems in place
- Payment methods

**Output:** Risk assessment, preventive recommendations

### Existing Business
- Monthly revenue
- Actual losses (refunds, returns, etc.)
- Operational metrics
- Billing errors
- Inventory issues

**Output:** Loss breakdown, recovery strategies

---

## 🤖 OpenAI Features

- Intelligent risk assessment
- Custom recovery strategies
- Industry-specific advice
- Implementation timelines
- ROI estimates
- Executive summaries

---

## ✅ Checklist

- [ ] OpenAI API key in `backend/.env`
- [ ] Backend starts: `cd backend && python -m uvicorn main:app --reload`
- [ ] Frontend starts: `cd frontend && npm run dev`
- [ ] Can access: http://localhost:5173
- [ ] New Business form works
- [ ] Existing Business form works
- [ ] Results display correctly

---

## 📚 Full Documentation

- **Setup Guide:** `BACKEND_SETUP_GUIDE.md`
- **Integration:** `FRONTEND_BACKEND_INTEGRATION.md`
- **Architecture:** `ARCHITECTURE_DIAGRAM.md`
- **Summary:** `INTEGRATION_SUMMARY.md`

---

## 🆘 Support

**Common Commands:**
```bash
# Start backend
cd backend
python -m uvicorn main:app --reload

# Start frontend
cd frontend
npm run dev

# Test
python test_business_analysis.py

# Check health
curl http://localhost:8000/health
```

**Get Help:**
- API Docs: http://localhost:8000/api/docs
- Check logs in terminal
- Review error messages

---

## 🎉 You're Ready!

Everything is set up and connected:
✅ Frontend → Backend → OpenAI → Results

**Next:** Add your OpenAI key and start analyzing!

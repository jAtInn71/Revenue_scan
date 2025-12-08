# 🚀 Quick Start Guide

## Backend Setup

### 1. Navigate to backend folder
```bash
cd backend
```

### 2. Create virtual environment
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key (optional)
# OPENAI_API_KEY=your_key_here
```

### 5. Run the server
```bash
python main.py
```

Backend will be available at: **http://localhost:8000**
API Docs: **http://localhost:8000/api/docs**

---

## Frontend Setup

### 1. Navigate to frontend folder
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Run development server
```bash
npm run dev
```

Frontend will be available at: **http://localhost:3000**

---

## 🎯 Usage

1. **Open browser** to `http://localhost:3000`
2. **Choose analysis type**: New Business or Existing Business
3. **Fill out the form** with your business details
4. **Get instant analysis** with AI-powered recommendations
5. **Download PDF report** with complete strategy

---

## 🔧 API Endpoints

### Business Analysis
- `POST /api/business/new/analyze` - Analyze new business
- `POST /api/business/existing/analyze` - Analyze existing business
- `GET /api/business/analysis/{id}` - Get analysis by ID

### Reports
- `POST /api/reports/generate` - Generate PDF report
- `GET /api/reports/download/{id}` - Download report

### Analytics
- `GET /api/analysis/statistics` - Platform statistics
- `GET /api/analysis/metrics/{id}` - Analysis metrics

---

## 📊 Features Implemented

✅ **Backend (FastAPI)**
- RESTful API with FastAPI
- SQLite database with SQLAlchemy
- AI-powered recommendations with OpenAI GPT
- Comprehensive business analysis engine
- PDF report generation with charts
- Risk assessment & scoring

✅ **Frontend (React)**
- Modern React with Vite
- Tailwind CSS styling
- Form validation with react-hook-form
- Charts with Recharts
- API integration with React Query
- Responsive design

✅ **Analysis Features**
- New business risk assessment
- Existing business leak detection
- 7+ leakage categories
- AI-powered recovery strategies
- Implementation timelines
- Expected recovery calculations

---

## 🎓 Perfect for Technical Events

This project demonstrates:
- ✅ Full-stack development
- ✅ AI integration
- ✅ Data analytics
- ✅ Business intelligence
- ✅ RESTful API design
- ✅ Modern frontend
- ✅ Real-world problem solving

---

## 📞 Support

For issues or questions, check:
- API Documentation: http://localhost:8000/api/docs
- README.md for detailed information
- Code comments for implementation details

---

**Built with ❤️ for Smart Revenue Protection** 📈

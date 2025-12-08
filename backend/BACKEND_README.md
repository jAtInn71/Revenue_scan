# Revenue Leakage System - Backend API

FastAPI-based backend with SQLite database, JWT authentication, and OpenAI integration.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

The `.env` file is already configured with your OpenAI API key. Review and update if needed:

```bash
# .env file settings
OPENAI_API_KEY=sk-proj-...  # Already configured
SECRET_KEY=your-secret-key   # Change in production
PORT=8000
```

### 3. Run the Server

```bash
# Option 1: Using Python directly
python main.py

# Option 2: Using Uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: **http://localhost:8000**

API Documentation: **http://localhost:8000/api/docs**

## 📡 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/me` - Update profile

### Dashboard
- `GET /api/dashboard/` - Get dashboard data (metrics, charts, alerts)
- `GET /api/dashboard/metrics` - Get key metrics

### Data Upload
- `POST /api/upload/` - Upload CSV/Excel file
- `GET /api/upload/history` - Get upload history
- `GET /api/upload/{upload_id}` - Get upload details

### AI Insights
- `POST /api/ai-insights/` - Chat with AI
- `POST /api/ai-insights/explain/{upload_id}` - Explain leakage

### Leakage Analysis
- `GET /api/analysis/leakage` - Get leakage data (filterable)
- `GET /api/analysis/leakage/{id}` - Get leakage detail
- `GET /api/analysis/summary` - Get analysis summary
- `GET /api/analysis/leakage/export` - Export data

### Alerts
- `GET /api/alerts/` - List all alerts
- `POST /api/alerts/` - Create alert
- `PUT /api/alerts/{id}` - Update alert
- `DELETE /api/alerts/{id}` - Delete alert
- `PATCH /api/alerts/{id}/status` - Toggle active/inactive

### Notifications
- `GET /api/notifications/` - Get notifications
- `PATCH /api/notifications/{id}/read` - Mark as read
- `POST /api/notifications/mark-all-read` - Mark all read
- `GET /api/notifications/unread-count` - Get unread count

### Reports
- `GET /api/reports/` - List all reports
- `POST /api/reports/generate` - Generate new report
- `GET /api/reports/{id}/download` - Download report
- `DELETE /api/reports/{id}` - Delete report

### Settings
- `GET /api/settings/profile` - Get user profile
- `PUT /api/settings/profile` - Update profile
- `POST /api/settings/change-password` - Change password
- `GET /api/settings/preferences` - Get preferences
- `PUT /api/settings/preferences` - Update preferences

## 🗄️ Database

SQLite database (`revenue_advisor.db`) includes:

- **users** - User accounts with authentication
- **business_analyses** - Revenue analysis records
- **uploaded_data** - CSV/Excel uploads and parsed data
- **alerts** - User-configured alert rules
- **notifications** - In-app notifications
- **reports** - Generated PDF reports

Database is automatically created on first run.

## 🔐 Authentication

Uses JWT (JSON Web Tokens) for authentication:

1. **Signup**: `POST /api/auth/signup`
   ```json
   {
     "email": "user@example.com",
     "password": "securepassword",
     "full_name": "John Doe",
     "company_name": "Acme Corp",
     "role": "Finance Manager"
   }
   ```

2. **Login**: `POST /api/auth/login`
   ```json
   {
     "email": "user@example.com",
     "password": "securepassword"
   }
   ```
   Returns: `{ "access_token": "...", "token_type": "bearer" }`

3. **Use Token**: Include in Authorization header
   ```
   Authorization: Bearer YOUR_TOKEN_HERE
   ```

## 🤖 OpenAI Integration

The system uses OpenAI GPT-4 for:

- **AI Chat Insights** - Intelligent Q&A about revenue data
- **Leakage Explanation** - Automated analysis of detected issues
- **Recommendations** - Smart suggestions for recovery

Your API key is already configured in `.env`:
```
OPENAI_API_KEY=sk-proj-KXpZ...
```

### AI Features:
- Analyzes uploaded transaction data
- Provides contextual recommendations
- Explains complex patterns in simple terms
- Suggests actionable recovery strategies

## 📤 File Upload

Supports CSV and Excel files:

**Endpoint**: `POST /api/upload/`

**Accepted formats**: `.csv`, `.xlsx`, `.xls`

**Max size**: 10MB

**Process**:
1. Upload file with optional column mapping
2. System parses data with pandas
3. Detects revenue leakages automatically
4. Returns analysis results

**Example**:
```python
files = {'file': open('transactions.csv', 'rb')}
data = {'column_mapping': json.dumps({
    'revenue': 'Total Amount',
    'date': 'Transaction Date'
})}
response = requests.post(
    'http://localhost:8000/api/upload/',
    files=files,
    data=data,
    headers={'Authorization': f'Bearer {token}'}
)
```

## 🔧 Configuration

Edit `backend/core/config.py` or `.env`:

```python
# API Settings
PORT = 8000
DEBUG = True

# Database
DATABASE_URL = "sqlite:///./revenue_advisor.db"

# OpenAI
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL = "gpt-4"

# JWT
SECRET_KEY = "your-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# File Upload
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = [".csv", ".xlsx", ".xls"]
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Test specific endpoint
pytest tests/test_auth.py
```

## 📊 Database Schema

### User
- email, hashed_password, full_name
- company_name, role, is_active
- created_at, last_login

### UploadedData
- upload_id, user_id, file_name
- column_mapping, total_rows
- leakage_data (JSON), status

### Alert
- alert_id, user_id, name
- metric, condition, threshold
- severity, is_active

### Notification
- notification_id, user_id
- title, message, severity
- is_read, created_at

### Report
- report_id, user_id, title
- category, date_range
- file_path, file_size

## 🚨 Error Handling

All endpoints return standard HTTP status codes:

- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success with no response
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid token
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "detail": "Error message here"
}
```

## 📝 Development Tips

1. **Auto-reload**: Use `--reload` flag for development
   ```bash
   uvicorn main:app --reload
   ```

2. **Interactive API Docs**: Visit `/api/docs` for Swagger UI

3. **Database Reset**: Delete `revenue_advisor.db` to start fresh

4. **Logs**: Check console output for errors and warnings

5. **CORS**: Frontend origins already configured in `.env`

## 🔗 Connect Frontend

Frontend should use base URL: `http://localhost:8000`

Update `frontend/src/services/apiService.js`:
```javascript
const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' }
});
```

## 📦 Project Structure

```
backend/
├── main.py                  # FastAPI app & routes
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
├── api/
│   └── routes/
│       ├── auth_routes.py        # Authentication
│       ├── dashboard_routes.py   # Dashboard data
│       ├── upload_routes.py      # File uploads
│       ├── ai_insights_routes.py # AI chat
│       ├── leakage_routes.py     # Analysis
│       ├── alert_routes.py       # Alerts
│       ├── notification_routes.py # Notifications
│       ├── reports_routes.py     # Reports
│       └── settings_routes.py    # User settings
├── core/
│   └── config.py            # Configuration
├── database/
│   └── database.py          # SQLAlchemy models
├── models/
│   └── schemas.py           # Pydantic models
└── services/
    ├── auth_service.py      # JWT & password hashing
    ├── ai_service.py        # OpenAI integration
    ├── analysis_service.py  # Revenue analysis
    └── report_service.py    # PDF generation
```

## ✅ Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Start backend: `python main.py`
3. ✅ Visit API docs: http://localhost:8000/api/docs
4. ✅ Test signup: Create a user account
5. ✅ Test login: Get auth token
6. ✅ Connect frontend: Update apiService.js base URL
7. ✅ Test upload: Upload a CSV file
8. ✅ Test AI chat: Ask AI about your data

## 🆘 Troubleshooting

**Import errors?**
```bash
pip install -r requirements.txt --upgrade
```

**Database errors?**
```bash
# Delete and recreate
rm revenue_advisor.db
python main.py
```

**OpenAI errors?**
- Check `.env` has valid API key
- Verify key at https://platform.openai.com/api-keys
- Check API usage limits

**CORS errors?**
- Update `ALLOWED_ORIGINS` in `.env`
- Add your frontend URL

**Port already in use?**
```bash
# Change port in .env
PORT=8001
```

---

**🎉 You're all set! Backend ready to integrate with your frontend.**

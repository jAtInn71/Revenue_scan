"""
Smart Revenue Leakage Advisor - Main FastAPI Application
AI-Powered System to Prevent and Recover Lost Revenue
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional
import uvicorn

from api.routes import (
    business_routes, 
    analysis_routes, 
    report_routes,
    auth_routes,
    dashboard_routes,
    upload_routes,
    ai_insights_routes,
    alert_routes,
    notification_routes,
    reports_routes,
    settings_routes,
    leakage_routes,
    chatbot_routes,
    user_routes
)
from core.config import settings
from database.database import init_db

# Initialize FastAPI app
app = FastAPI(
    title="Smart Revenue Leakage Advisor API",
    description="AI-Powered Revenue Loss Prevention and Recovery System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Database initialized successfully")
    print(f"🚀 Server running on {settings.HOST}:{settings.PORT}")

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "active",
        "message": "Smart Revenue Leakage Advisor API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Revenue Leakage Advisor",
        "database": "connected"
    }

# Include routers
# Authentication
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])

# Admin & User Management
app.include_router(user_routes.router, prefix="/api/admin", tags=["Admin"])

# Dashboard & Analytics
app.include_router(dashboard_routes.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(leakage_routes.router, prefix="/api/analysis", tags=["Analysis"])

# Data Management
app.include_router(upload_routes.router, prefix="/api/upload", tags=["Upload"])
app.include_router(ai_insights_routes.router, prefix="/api/ai-insights", tags=["AI Insights"])
app.include_router(chatbot_routes.router, prefix="/api/chatbot", tags=["AI Chatbot"])

# Alerts & Notifications
app.include_router(alert_routes.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(notification_routes.router, prefix="/api/notifications", tags=["Notifications"])

# Reports & Settings
app.include_router(reports_routes.router, prefix="/api/reports", tags=["Reports"])
app.include_router(settings_routes.router, prefix="/api/settings", tags=["Settings"])

# Legacy routes (keep for backward compatibility)
app.include_router(business_routes.router, prefix="/api/business", tags=["Business"])
app.include_router(analysis_routes.router, prefix="/api/analysis-old", tags=["Analysis Old"])
app.include_router(report_routes.router, prefix="/api/reports-old", tags=["Reports Old"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

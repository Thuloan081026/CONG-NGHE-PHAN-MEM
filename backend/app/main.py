from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core.database import engine, Base
import traceback
import os
from pathlib import Path

# Import all routers
from .api.v1 import auth as auth_router
from .api.v1 import user as user_router
from .api.v1 import syllabus as syllabus_router
from .api.v1 import workflow as workflow_router
from .api.v1 import review as review_router
from .api.v1 import clo_plo as clo_plo_router
from .api.v1 import search as search_router
from .api.v1 import ai as ai_router
from .api.v1 import notification as notification_router
from .api.v1 import settings as settings_router
from .api.v1 import audit_logs as audit_logs_router
from .api.v1 import admin as admin_router
from .api.v1 import student as student_router
from .api.v1 import principal as principal_router
from .api import departments as departments_router
from .api import users_import as users_import_router

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMD Backend - Syllabus Management System",
    description="Backend API for Syllabus Management & Digitalization System"
)

# Startup event: Tự động tạo tài khoản demo khi khởi động
@app.on_event("startup")
async def startup_event():
    """Khởi tạo dữ liệu demo khi server khởi động"""
    from .core.database import initialize_demo_users
    initialize_demo_users()

# CORS Configuration for Frontend - Allow all for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Login page
        "http://127.0.0.1:3000",      # Login page alternative
        "http://localhost:3001",      # Admin dashboard
        "http://127.0.0.1:3001",      # Admin dashboard alternative
        "http://localhost:3002",      # Lecturer dashboard
        "http://127.0.0.1:3002",      # Lecturer dashboard alternative
        "http://localhost:3003",      # Principal dashboard
        "http://127.0.0.1:3003",      # Principal dashboard alternative
        "http://localhost:8000",      # Backend API docs
        "*"                           # Allow all for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Global exception handler for debugging
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_detail = f"{type(exc).__name__}: {str(exc)}"
    traceback_str = traceback.format_exc()
    print(f"[ERROR] {error_detail}")
    print(f"[TRACEBACK] {traceback_str}")
    return JSONResponse(
        status_code=500,
        content={"detail": error_detail, "traceback": traceback_str}
    )

@app.get("/")
def root():
    return {"message": "Syllabus Management API", "status": "running"}

@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint working", "status": "success"}

# Include all routers
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(syllabus_router.router)
app.include_router(workflow_router.router)
app.include_router(review_router.router)
app.include_router(clo_plo_router.router)
app.include_router(search_router.router)
app.include_router(ai_router.router)
app.include_router(notification_router.router)
app.include_router(settings_router.router)
app.include_router(audit_logs_router.router)
app.include_router(admin_router.router)
app.include_router(student_router.router)
app.include_router(principal_router.router)
app.include_router(departments_router.router, prefix="/departments", tags=["departments"])
app.include_router(users_import_router.router, prefix="/users/import", tags=["users-import"])

# Mount static files for uploaded syllabus files
data_dir = str(Path(__file__).resolve().parents[1] / "data")
os.makedirs(data_dir, exist_ok=True)
app.mount("/data", StaticFiles(directory=data_dir), name="data")

# Serve frontend static files from the workspace so users can open the UI from backend origin
try:
    frontend_dir = str(Path(__file__).resolve().parents[2] / "frontend")
    if os.path.isdir(frontend_dir):
        app.mount("/ui", StaticFiles(directory=frontend_dir, html=True), name="frontend")
    else:
        print(f"[WARN] Frontend directory not found: {frontend_dir}")
except Exception as _e:
    print("[WARN] Could not mount frontend static files:", _e)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Backend API is running"}

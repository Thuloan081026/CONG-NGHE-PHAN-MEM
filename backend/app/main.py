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
    from .core.database import SessionLocal
    from .models.user import User
    from .core.security import get_password_hash
    
    db = SessionLocal()
    try:
        # Kiểm tra xem đã có user nào chưa
        user_count = db.query(User).count()
        if user_count > 0:
            print("✓ Đã có tài khoản trong hệ thống")
            return
        
        # Danh sách tài khoản demo với email @edu.vn
        demo_users = [
            {"email": "admin@edu.vn", "full_name": "Quản trị viên hệ thống", "password": "admin123", "role": "admin"},
            {"email": "lecturer@edu.vn", "full_name": "Giảng viên Demo", "password": "lecturer123", "role": "lecturer"},
            {"email": "hod@edu.vn", "full_name": "Trưởng khoa CNTT", "password": "hod123", "role": "hod"},
            {"email": "aa@edu.vn", "full_name": "Phòng Đào tạo", "password": "aa123", "role": "academic_affairs"},
            {"email": "student@edu.vn", "full_name": "Sinh viên Demo", "password": "student123", "role": "student"},
        ]
        
        print("\n👥 Đang tạo tài khoản demo...")
        for user_data in demo_users:
            # Kiểm tra từng user trước khi tạo
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                user = User(
                    email=user_data["email"],
                    full_name=user_data["full_name"],
                    hashed_password=get_password_hash(user_data["password"]),
                    role=user_data["role"],
                    is_active=True
                )
                db.add(user)
                print(f"  ✅ {user_data['email']} / {user_data['password']}")
        
        db.commit()
        print("✨ Tài khoản demo đã được tạo tự động!\n")
    except Exception as e:
        print(f"⚠️ Lỗi khi tạo tài khoản demo: {e}")
        db.rollback()
    finally:
        db.close()

# CORS Configuration for Frontend - Allow all for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
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

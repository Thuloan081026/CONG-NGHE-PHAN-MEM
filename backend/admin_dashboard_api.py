"""
Admin Dashboard API - Get real-time statistics from database
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

Base = declarative_base()
router = APIRouter()

# Pydantic Models
class DashboardStats(BaseModel):
    total_users: int = 0
    total_syllabuses: int = 0
    pending_review: int = 0
    published: int = 0
    draft: int = 0
    total_reviews: int = 0
    admin_count: int = 0
    lecturer_count: int = 0
    hod_count: int = 0
    aa_count: int = 0

class RecentActivity(BaseModel):
    id: int
    action: str
    description: str
    user_name: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class DashboardResponse(BaseModel):
    stats: DashboardStats
    recent_activities: list[RecentActivity] = []

# Database dependency
def get_db():
    DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mock current user (should validate JWT token)
def get_current_admin():
    return {"user_id": 26, "email": "admin@hcmute.edu.vn", "role": "admin"}

@router.get("/admin/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin)
):
    """Get real-time dashboard statistics from database"""
    try:
        stats = DashboardStats()
        
        # Count total users
        result = db.execute(text("SELECT COUNT(*) as count FROM users"))
        stats.total_users = result.fetchone()[0]
        
        # Count total syllabuses
        result = db.execute(text("SELECT COUNT(*) as count FROM syllabuses"))
        stats.total_syllabuses = result.fetchone()[0]
        
        # Count by status
        result = db.execute(text("SELECT COUNT(*) as count FROM syllabuses WHERE status = 'pending_review'"))
        stats.pending_review = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM syllabuses WHERE status = 'published'"))
        stats.published = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM syllabuses WHERE status = 'draft'"))
        stats.draft = result.fetchone()[0]
        
        # Count reviews
        result = db.execute(text("SELECT COUNT(*) as count FROM reviews"))
        stats.total_reviews = result.fetchone()[0]
        
        # Count users by role
        result = db.execute(text("SELECT COUNT(*) as count FROM users WHERE role = 'admin'"))
        stats.admin_count = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM users WHERE role = 'lecturer'"))
        stats.lecturer_count = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM users WHERE role = 'hod'"))
        stats.hod_count = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM users WHERE role = 'academic_affairs'"))
        stats.aa_count = result.fetchone()[0]
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Test function
def test_api():
    """Test the admin dashboard API"""
    DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("\n=== Testing Admin Dashboard API ===\n")
        
        # Get statistics
        stats = DashboardStats()
        
        result = db.execute(text("SELECT COUNT(*) as count FROM users"))
        stats.total_users = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM syllabuses"))
        stats.total_syllabuses = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM syllabuses WHERE status = 'pending_review'"))
        stats.pending_review = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM syllabuses WHERE status = 'published'"))
        stats.published = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM syllabuses WHERE status = 'draft'"))
        stats.draft = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM reviews"))
        stats.total_reviews = result.fetchone()[0]
        
        # Count by role
        result = db.execute(text("SELECT COUNT(*) as count FROM users WHERE role = 'admin'"))
        stats.admin_count = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM users WHERE role = 'lecturer'"))
        stats.lecturer_count = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM users WHERE role = 'hod'"))
        stats.hod_count = result.fetchone()[0]
        
        result = db.execute(text("SELECT COUNT(*) as count FROM users WHERE role = 'academic_affairs'"))
        stats.aa_count = result.fetchone()[0]
        
        print("📊 Dashboard Statistics (from database):")
        print(f"   Total Users: {stats.total_users}")
        print(f"     - Admins: {stats.admin_count}")
        print(f"     - Lecturers: {stats.lecturer_count}")
        print(f"     - HODs: {stats.hod_count}")
        print(f"     - Academic Affairs: {stats.aa_count}")
        print(f"\n   Total Syllabuses: {stats.total_syllabuses}")
        print(f"     - Published: {stats.published}")
        print(f"     - Pending Review: {stats.pending_review}")
        print(f"     - Draft: {stats.draft}")
        print(f"\n   Total Reviews: {stats.total_reviews}")
        
        print("\n✅ API endpoint ready:")
        print("   GET /api/admin/dashboard/stats")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_api()

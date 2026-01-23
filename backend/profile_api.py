"""
Profile API - Get lecturer profile data from database
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Date, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

Base = declarative_base()
router = APIRouter()

# Database Models
class LecturerProfile(Base):
    __tablename__ = "lecturer_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    date_of_birth = Column(Date)
    gender = Column(String(10))
    address = Column(Text)
    lecturer_code = Column(String(50))
    department = Column(String(255))
    position = Column(String(100))
    degree = Column(String(100))
    specialization = Column(String(255))
    start_year = Column(Integer)
    employment_status = Column(String(50), default='active')
    total_syllabuses = Column(Integer, default=0)
    published_syllabuses = Column(Integer, default=0)
    pending_reviews = Column(Integer, default=0)
    years_experience = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class Education(Base):
    __tablename__ = "lecturer_education"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    degree = Column(String(255), nullable=False)
    field = Column(String(255))
    school = Column(String(255), nullable=False)
    start_year = Column(Integer)
    end_year = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)

# Pydantic Models
class EducationResponse(BaseModel):
    degree: str
    field: Optional[str] = None
    school: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class ProfileResponse(BaseModel):
    # Personal Info
    full_name: str
    email: str  # From user table
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    
    # Professional Info
    lecturer_code: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    degree: Optional[str] = None
    specialization: Optional[str] = None
    start_year: Optional[int] = None
    employment_status: Optional[str] = None
    
    # Statistics
    total_syllabuses: int = 0
    published_syllabuses: int = 0
    pending_reviews: int = 0
    years_experience: int = 0
    
    # Education
    education: List[EducationResponse] = []

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

# Mock current user (should be from JWT token)
def get_current_user():
    return {"user_id": 53, "email": "nguyen.dat@university.edu.vn"}

@router.get("/lecturers/profile", response_model=ProfileResponse)
async def get_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get lecturer profile data"""
    try:
        # Get profile
        profile = db.query(LecturerProfile).filter(
            LecturerProfile.user_id == current_user["user_id"]
        ).first()
        
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Get education records
        education_records = db.query(Education).filter(
            Education.user_id == current_user["user_id"]
        ).order_by(Education.end_year.desc()).all()
        
        # Format date of birth
        dob_str = None
        if profile.date_of_birth:
            dob_str = profile.date_of_birth.strftime("%d/%m/%Y")
        
        # Build response
        response = ProfileResponse(
            full_name=profile.full_name,
            email=current_user["email"],
            phone=profile.phone,
            date_of_birth=dob_str,
            gender=profile.gender,
            address=profile.address,
            lecturer_code=profile.lecturer_code,
            department=profile.department,
            position=profile.position,
            degree=profile.degree,
            specialization=profile.specialization,
            start_year=profile.start_year,
            employment_status=profile.employment_status,
            total_syllabuses=profile.total_syllabuses,
            published_syllabuses=profile.published_syllabuses,
            pending_reviews=profile.pending_reviews,
            years_experience=profile.years_experience,
            education=[
                EducationResponse(
                    degree=edu.degree,
                    field=edu.field,
                    school=edu.school,
                    start_year=edu.start_year,
                    end_year=edu.end_year
                )
                for edu in education_records
            ]
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Test function
def test_api():
    """Test the profile API"""
    DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("\n=== Testing Profile API ===\n")
        
        user_id = 53
        
        # Get profile
        profile = db.query(LecturerProfile).filter(
            LecturerProfile.user_id == user_id
        ).first()
        
        if profile:
            print(f"✅ Profile found for {profile.full_name}")
            print(f"   Department: {profile.department}")
            print(f"   Position: {profile.position}")
            print(f"   Degree: {profile.degree}")
            print(f"   Specialization: {profile.specialization}")
            print(f"   Total Syllabuses: {profile.total_syllabuses}")
            print(f"   Published: {profile.published_syllabuses}")
            print(f"   Pending: {profile.pending_reviews}")
            print(f"   Experience: {profile.years_experience} years")
        
        # Get education
        education = db.query(Education).filter(
            Education.user_id == user_id
        ).order_by(Education.end_year.desc()).all()
        
        print(f"\n✅ Found {len(education)} education records:")
        for edu in education:
            print(f"   {edu.degree} - {edu.field} ({edu.start_year}-{edu.end_year})")
            print(f"   {edu.school}")
        
        print("\n✅ API endpoint ready:")
        print("   GET /api/lecturers/profile")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_api()

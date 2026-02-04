"""
Populate lecturer profile data for user_id 53
"""
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date

Base = declarative_base()

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
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

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

def populate_data():
    """Populate profile data for user_id 53"""
    DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("\n=== Populating Profile Data ===\n")
        
        user_id = 53
        
        # Check if profile already exists
        existing_profile = db.query(LecturerProfile).filter(
            LecturerProfile.user_id == user_id
        ).first()
        
        if existing_profile:
            print(f"Profile already exists for user_id {user_id}, updating...")
            existing_profile.full_name = "Nguyễn Văn Đạt"
            existing_profile.phone = "+84 123 456 789"
            existing_profile.date_of_birth = date(1985, 3, 15)
            existing_profile.gender = "Nam"
            existing_profile.address = "123 Đường ABC, Quận 1, TP.HCM"
            existing_profile.lecturer_code = "LT2018001"
            existing_profile.department = "Khoa Công nghệ Thông tin"
            existing_profile.position = "Giảng viên"
            existing_profile.degree = "Tiến sĩ"
            existing_profile.specialization = "Trí tuệ nhân tạo, Machine Learning"
            existing_profile.start_year = 2018
            existing_profile.employment_status = "Đang làm việc"
            existing_profile.total_syllabuses = 12
            existing_profile.published_syllabuses = 8
            existing_profile.pending_reviews = 3
            existing_profile.years_experience = 7
            existing_profile.updated_at = datetime.now()
        else:
            # Create profile
            profile = LecturerProfile(
                user_id=user_id,
                full_name="Nguyễn Văn Đạt",
                phone="+84 123 456 789",
                date_of_birth=date(1985, 3, 15),
                gender="Nam",
                address="123 Đường ABC, Quận 1, TP.HCM",
                lecturer_code="LT2018001",
                department="Khoa Công nghệ Thông tin",
                position="Giảng viên",
                degree="Tiến sĩ",
                specialization="Trí tuệ nhân tạo, Machine Learning",
                start_year=2018,
                employment_status="Đang làm việc",
                total_syllabuses=12,
                published_syllabuses=8,
                pending_reviews=3,
                years_experience=7
            )
            db.add(profile)
        
        db.commit()
        print("✅ Profile data saved")
        
        # Delete existing education records
        db.query(Education).filter(Education.user_id == user_id).delete()
        
        # Add education records
        educations = [
            Education(
                user_id=user_id,
                degree="Tiến sĩ",
                field="Khoa học Máy tính",
                school="Đại học Stanford, Mỹ",
                start_year=2015,
                end_year=2018
            ),
            Education(
                user_id=user_id,
                degree="Thạc sĩ",
                field="Công nghệ Thông tin",
                school="Đại học Quốc gia TP.HCM",
                start_year=2010,
                end_year=2012
            ),
            Education(
                user_id=user_id,
                degree="Cử nhân",
                field="Khoa học Máy tính",
                school="Đại học Bách Khoa TP.HCM",
                start_year=2003,
                end_year=2007
            )
        ]
        
        for edu in educations:
            db.add(edu)
        
        db.commit()
        print(f"✅ Added {len(educations)} education records")
        
        # Verify data
        print("\n=== Verification ===")
        profile = db.query(LecturerProfile).filter(
            LecturerProfile.user_id == user_id
        ).first()
        
        if profile:
            print(f"\nProfile for {profile.full_name}:")
            print(f"  Email: nguyen.dat@university.edu.vn")
            print(f"  Phone: {profile.phone}")
            print(f"  Department: {profile.department}")
            print(f"  Position: {profile.position}")
            print(f"  Degree: {profile.degree}")
            print(f"  Specialization: {profile.specialization}")
        
        edu_count = db.query(Education).filter(Education.user_id == user_id).count()
        print(f"\nEducation records: {edu_count}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    populate_data()

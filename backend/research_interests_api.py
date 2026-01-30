"""
Research Interests API - CRUD operations for lecturer research interests
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create Base for SQLAlchemy models
Base = declarative_base()

router = APIRouter()

# Pydantic models for request/response
class ResearchInterestCreate(BaseModel):
    interest_name: str

class ResearchInterestResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ResearchInterestsListResponse(BaseModel):
    interests: List[ResearchInterestResponse]
    total: int

# SQLAlchemy model
class ResearchInterest(Base):
    __tablename__ = "research_interests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    interest_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Dependency to get database session
def get_db():
    DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get current user (simplified - should validate JWT token)
def get_current_user():
    # TODO: Implement proper JWT validation
    # For now, return demo user_id
    return {"user_id": 53, "email": "nguyen.dat@university.edu.vn"}

@router.get("/lecturers/research-interests", response_model=ResearchInterestsListResponse)
async def get_research_interests(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all research interests for current user"""
    try:
        interests = db.query(ResearchInterest).filter(
            ResearchInterest.user_id == current_user["user_id"]
        ).order_by(ResearchInterest.created_at.desc()).all()
        
        interests_list = [
            ResearchInterestResponse(
                id=interest.id,
                name=interest.interest_name,
                created_at=interest.created_at
            )
            for interest in interests
        ]
        
        return ResearchInterestsListResponse(
            interests=interests_list,
            total=len(interests_list)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/lecturers/research-interests", response_model=ResearchInterestResponse)
async def add_research_interest(
    interest_data: ResearchInterestCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add a new research interest for current user"""
    try:
        # Check if interest already exists for this user
        existing = db.query(ResearchInterest).filter(
            ResearchInterest.user_id == current_user["user_id"],
            ResearchInterest.interest_name == interest_data.interest_name
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Lĩnh vực này đã tồn tại")
        
        # Create new interest
        new_interest = ResearchInterest(
            user_id=current_user["user_id"],
            interest_name=interest_data.interest_name,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.add(new_interest)
        db.commit()
        db.refresh(new_interest)
        
        return ResearchInterestResponse(
            id=new_interest.id,
            name=new_interest.interest_name,
            created_at=new_interest.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/lecturers/research-interests/{interest_id}")
async def delete_research_interest(
    interest_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a research interest"""
    try:
        # Find the interest
        interest = db.query(ResearchInterest).filter(
            ResearchInterest.id == interest_id,
            ResearchInterest.user_id == current_user["user_id"]
        ).first()
        
        if not interest:
            raise HTTPException(status_code=404, detail="Không tìm thấy lĩnh vực này")
        
        db.delete(interest)
        db.commit()
        
        return {"message": "Xóa lĩnh vực thành công", "id": interest_id}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Test function
def test_api():
    """Test the research interests API"""
    DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    
    try:
        print("\n=== Testing Research Interests API ===\n")
        
        # Test GET
        print("1. Getting research interests for user_id 53...")
        interests = db.query(ResearchInterest).filter(
            ResearchInterest.user_id == 53
        ).all()
        
        print(f"Found {len(interests)} interests:")
        for interest in interests:
            print(f"  - ID: {interest.id}, Name: {interest.interest_name}")
        
        print("\n✅ API endpoints ready to use!")
        print("\nEndpoints:")
        print("  GET    /api/lecturers/research-interests")
        print("  POST   /api/lecturers/research-interests")
        print("  DELETE /api/lecturers/research-interests/{id}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_api()

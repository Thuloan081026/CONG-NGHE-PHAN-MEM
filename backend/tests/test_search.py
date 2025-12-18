"""
Tests for Search Module (Module 6)
Tests search functionality, filters, and full-text search
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

# Import Base first, then all models
from app.core.database import Base
from app import models  # Import all models from package
from app.models.user import User
from app.models.syllabus import Syllabus
from app.services.search_service import SearchService


# MySQL XAMPP connection
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Session:
    """Create test database session"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Clean up existing test data
    db.query(Syllabus).delete()
    db.query(User).delete()
    db.commit()
    
    yield db
    
    # Clean up after test
    db.query(Syllabus).delete()
    db.query(User).delete()
    db.commit()
    db.close()


@pytest.fixture(scope="function")
def setup_test_data(db: Session):
    """Setup test data with multiple syllabuses for search testing"""
    
    # Create test user
    user = User(
        email="lecturer@test.com",
        full_name="Test Lecturer",
        hashed_password="test_hash",
        role="lecturer"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create multiple syllabuses with different attributes
    syllabuses = [
        # Computer Science courses
        Syllabus(
            subject_code="CS101",
            subject_name="Introduction to Programming",
            description="Basic programming concepts",
            department="Computer Science",
            semester=1,
            credits=3,
            academic_year="2024-2025",
            objectives="Learn programming fundamentals",
            content="Variables, loops, functions, OOP",
            teaching_methods="Lectures and lab sessions",
            assessment_methods="Assignments and exams",
            created_by=user.id,
            status="published",
            is_published=True,
            published_at=datetime.utcnow()
        ),
        Syllabus(
            subject_code="CS201",
            subject_name="Data Structures and Algorithms",
            description="Advanced data structures",
            department="Computer Science",
            semester=3,
            credits=4,
            academic_year="2024-2025",
            objectives="Master data structures",
            content="Arrays, linked lists, trees, graphs, sorting algorithms",
            teaching_methods="Interactive lectures",
            assessment_methods="Projects and exams",
            created_by=user.id,
            status="published",
            is_published=True,
            published_at=datetime.utcnow()
        ),
        Syllabus(
            subject_code="CS301",
            subject_name="Database Systems",
            description="Database design and SQL",
            department="Computer Science",
            semester=5,
            credits=3,
            academic_year="2025-2026",
            objectives="Understand database concepts",
            content="SQL, normalization, transactions, query optimization",
            teaching_methods="Theory and practical",
            assessment_methods="Labs and final exam",
            created_by=user.id,
            status="published",
            is_published=True,
            published_at=datetime.utcnow()
        ),
        # Mathematics courses
        Syllabus(
            subject_code="MATH101",
            subject_name="Calculus I",
            description="Differential calculus",
            department="Mathematics",
            semester=1,
            credits=4,
            academic_year="2024-2025",
            objectives="Master derivatives and limits",
            content="Limits, derivatives, applications of derivatives",
            teaching_methods="Lectures and problem solving",
            assessment_methods="Weekly quizzes and exams",
            created_by=user.id,
            status="published",
            is_published=True,
            published_at=datetime.utcnow()
        ),
        Syllabus(
            subject_code="MATH201",
            subject_name="Linear Algebra",
            description="Matrices and vector spaces",
            department="Mathematics",
            semester=2,
            credits=3,
            academic_year="2024-2025",
            objectives="Understand linear transformations",
            content="Matrices, determinants, eigenvalues, vector spaces",
            teaching_methods="Theoretical and computational",
            assessment_methods="Problem sets and exams",
            created_by=user.id,
            status="published",
            is_published=True,
            published_at=datetime.utcnow()
        ),
        # Draft syllabus (not published)
        Syllabus(
            subject_code="CS401",
            subject_name="Machine Learning",
            description="Introduction to ML",
            department="Computer Science",
            semester=7,
            credits=3,
            academic_year="2025-2026",
            objectives="Learn ML algorithms",
            content="Supervised learning, neural networks",
            teaching_methods="Lectures and projects",
            assessment_methods="Project-based",
            created_by=user.id,
            status="draft",
            is_published=False
        )
    ]
    
    for syllabus in syllabuses:
        db.add(syllabus)
    
    db.commit()
    
    return {
        "user": user,
        "syllabuses": syllabuses
    }


# ==================== BASIC SEARCH TESTS ====================

def test_search_by_subject_name(db: Session, setup_test_data):
    """Test search by subject name"""
    service = SearchService(db)
    
    # Search for "Programming"
    result = service.search_syllabuses(query="Programming")
    
    assert result["total"] == 1
    assert result["results"][0].subject_code == "CS101"
    assert "Programming" in result["results"][0].subject_name


def test_search_by_subject_code(db: Session, setup_test_data):
    """Test search by subject code"""
    service = SearchService(db)
    
    # Search for "CS201"
    result = service.search_syllabuses(query="CS201")
    
    assert result["total"] == 1
    assert result["results"][0].subject_code == "CS201"


def test_search_case_insensitive(db: Session, setup_test_data):
    """Test that search is case-insensitive"""
    service = SearchService(db)
    
    # Search with different cases
    result1 = service.search_syllabuses(query="calculus")
    result2 = service.search_syllabuses(query="CALCULUS")
    result3 = service.search_syllabuses(query="Calculus")
    
    assert result1["total"] == result2["total"] == result3["total"] == 1


def test_search_partial_match(db: Session, setup_test_data):
    """Test partial matching in search"""
    service = SearchService(db)
    
    # Search for "Data" should match "Data Structures" and "Database"
    result = service.search_syllabuses(query="Data")
    
    assert result["total"] == 2
    codes = [s.subject_code for s in result["results"]]
    assert "CS201" in codes
    assert "CS301" in codes


# ==================== FILTER TESTS ====================

def test_filter_by_department(db: Session, setup_test_data):
    """Test filtering by department"""
    service = SearchService(db)
    
    # Filter Computer Science
    result = service.search_syllabuses(department="Computer Science")
    
    assert result["total"] == 3  # CS101, CS201, CS301 (CS401 is draft)
    for syllabus in result["results"]:
        assert syllabus.department == "Computer Science"


def test_filter_by_semester(db: Session, setup_test_data):
    """Test filtering by semester"""
    service = SearchService(db)
    
    # Filter semester 1
    result = service.search_syllabuses(semester=1)
    
    assert result["total"] == 2  # CS101 and MATH101
    for syllabus in result["results"]:
        assert syllabus.semester == 1


def test_filter_by_academic_year(db: Session, setup_test_data):
    """Test filtering by academic year"""
    service = SearchService(db)
    
    # Filter 2025-2026
    result = service.search_syllabuses(academic_year="2025-2026")
    
    assert result["total"] == 1  # Only CS301
    assert result["results"][0].subject_code == "CS301"


def test_multiple_filters_combined(db: Session, setup_test_data):
    """Test combining multiple filters"""
    service = SearchService(db)
    
    # Search in Computer Science, semester 1
    result = service.search_syllabuses(
        department="Computer Science",
        semester=1
    )
    
    assert result["total"] == 1
    assert result["results"][0].subject_code == "CS101"


# ==================== FULL-TEXT SEARCH TESTS ====================

def test_full_text_search_in_objectives(db: Session, setup_test_data):
    """Test full-text search in objectives field"""
    service = SearchService(db)
    
    # Search for "fundamentals" (in CS101 objectives)
    result = service.search_syllabuses(full_text="fundamentals")
    
    assert result["total"] == 1
    assert result["results"][0].subject_code == "CS101"


def test_full_text_search_in_content(db: Session, setup_test_data):
    """Test full-text search in content field"""
    service = SearchService(db)
    
    # Search for "algorithms" (in CS201 content)
    result = service.search_syllabuses(full_text="algorithms")
    
    assert result["total"] == 1
    assert result["results"][0].subject_code == "CS201"


def test_full_text_search_multiple_fields(db: Session, setup_test_data):
    """Test full-text search across multiple fields"""
    service = SearchService(db)
    
    # Search for "SQL" (in CS301 description and content)
    result = service.search_syllabuses(full_text="SQL")
    
    assert result["total"] == 1
    assert result["results"][0].subject_code == "CS301"


def test_full_text_with_filter(db: Session, setup_test_data):
    """Test combining full-text search with filters"""
    service = SearchService(db)
    
    # Search for "exams" in Mathematics department
    result = service.search_syllabuses(
        full_text="exams",
        department="Mathematics"
    )
    
    assert result["total"] == 2  # MATH101 and MATH201


# ==================== STATUS FILTER TESTS ====================

def test_only_published_by_default(db: Session, setup_test_data):
    """Test that only published syllabuses are returned by default"""
    service = SearchService(db)
    
    # Search all Computer Science courses
    result = service.search_syllabuses(department="Computer Science")
    
    # Should not include CS401 (draft)
    assert result["total"] == 3
    codes = [s.subject_code for s in result["results"]]
    assert "CS401" not in codes


def test_search_draft_syllabuses(db: Session, setup_test_data):
    """Test searching draft syllabuses explicitly"""
    service = SearchService(db)
    
    # Search draft status
    result = service.search_syllabuses(
        department="Computer Science",
        status="draft"
    )
    
    assert result["total"] == 1
    assert result["results"][0].subject_code == "CS401"
    assert result["results"][0].is_published == False


# ==================== PAGINATION TESTS ====================

def test_pagination_limit(db: Session, setup_test_data):
    """Test pagination limit parameter"""
    service = SearchService(db)
    
    # Get only 2 results
    result = service.search_syllabuses(limit=2)
    
    assert len(result["results"]) == 2
    assert result["limit"] == 2


def test_pagination_skip(db: Session, setup_test_data):
    """Test pagination skip parameter"""
    service = SearchService(db)
    
    # Get first page
    page1 = service.search_syllabuses(limit=2, skip=0)
    
    # Get second page
    page2 = service.search_syllabuses(limit=2, skip=2)
    
    # Results should be different
    assert page1["results"][0].id != page2["results"][0].id
    assert page1["skip"] == 0
    assert page2["skip"] == 2


# ==================== HELPER FUNCTION TESTS ====================

def test_get_search_filters(db: Session, setup_test_data):
    """Test getting available filter options"""
    service = SearchService(db)
    
    filters = service.get_search_filters()
    
    assert "departments" in filters
    assert "semesters" in filters
    assert "academic_years" in filters
    
    # Check departments
    assert "Computer Science" in filters["departments"]
    assert "Mathematics" in filters["departments"]
    
    # Check semesters
    assert 1 in filters["semesters"]
    assert 3 in filters["semesters"]
    
    # Check academic years
    assert "2024-2025" in filters["academic_years"]
    assert "2025-2026" in filters["academic_years"]


def test_search_by_code(db: Session, setup_test_data):
    """Test searching by exact subject code"""
    service = SearchService(db)
    
    syllabus = service.search_by_code("CS101")
    
    assert syllabus is not None
    assert syllabus.subject_code == "CS101"
    assert syllabus.is_published == True


def test_search_by_code_not_found(db: Session, setup_test_data):
    """Test searching for non-existent code"""
    service = SearchService(db)
    
    syllabus = service.search_by_code("NONEXIST999")
    
    assert syllabus is None


def test_search_by_code_draft(db: Session, setup_test_data):
    """Test that draft syllabuses are not returned by code search"""
    service = SearchService(db)
    
    # CS401 exists but is draft
    syllabus = service.search_by_code("CS401")
    
    assert syllabus is None  # Should not find draft


def test_get_related_syllabuses(db: Session, setup_test_data):
    """Test getting related syllabuses"""
    service = SearchService(db)
    
    # Get CS101
    cs101 = service.search_by_code("CS101")
    
    # Get related syllabuses
    related = service.get_related_syllabuses(cs101.id, limit=3)
    
    assert len(related) > 0
    # Should include other CS courses or semester 1 courses
    for syllabus in related:
        assert syllabus.id != cs101.id
        assert (syllabus.department == "Computer Science" or 
                syllabus.semester == 1)


def test_get_popular_syllabuses(db: Session, setup_test_data):
    """Test getting popular (recently published) syllabuses"""
    service = SearchService(db)
    
    popular = service.get_popular_syllabuses(limit=3)
    
    assert len(popular) == 3
    # All should be published
    for syllabus in popular:
        assert syllabus.is_published == True


# ==================== EDGE CASES ====================

def test_search_empty_query(db: Session, setup_test_data):
    """Test search with no query returns all published syllabuses"""
    service = SearchService(db)
    
    result = service.search_syllabuses()
    
    # Should return all 5 published syllabuses
    assert result["total"] == 5


def test_search_no_results(db: Session, setup_test_data):
    """Test search with no matching results"""
    service = SearchService(db)
    
    result = service.search_syllabuses(query="NONEXISTENT_COURSE")
    
    assert result["total"] == 0
    assert len(result["results"]) == 0


def test_filter_combination_no_results(db: Session, setup_test_data):
    """Test filter combination that yields no results"""
    service = SearchService(db)
    
    # Mathematics in semester 7 - doesn't exist
    result = service.search_syllabuses(
        department="Mathematics",
        semester=7
    )
    
    assert result["total"] == 0

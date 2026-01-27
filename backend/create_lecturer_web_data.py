"""
Create comprehensive demo data for Lecturer Web Interface
Generates demo syllabuses, reviews, notifications, and profile data
"""
import sys
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, UTC
import json

from app.core.database import engine, SessionLocal
from app.models.user import User
from app.models.syllabus import Syllabus, SyllabusVersion
from app.models.clo import CLO
from app.models.review import Review
from app.models.notification import Notification
from app.core.security import get_password_hash

def create_lecturer_profiles(db: Session):
    """Create detailed lecturer profiles"""
    print("\n📚 Creating Lecturer Profiles...")
    
    lecturers_data = [
        {
            "email": "lecturer1@hcmute.edu.vn",
            "full_name": "Ts. Trần Thị Bích",
            "employee_id": "GV001",
            "degree": "Tiến sĩ Khoa học Máy tính",
            "title": "Tiến sĩ",
            "department": "Bộ môn Khoa học Máy tính",
            "specialization": "Trí tuệ nhân tạo, Machine Learning",
            "phone": "0123456789",
            "office_location": "A4-302",
            "research_interests": "Xử lý ngôn ngữ tự nhiên, Deep Learning, Computer Vision",
            "teaching_subjects": "Nhập môn lập trình, Cấu trúc dữ liệu, Trí tuệ nhân tạo",
            "years_experience": 8,
            "qualifications": "PhD Computer Science (2020) - University of Technology\nMaster of Science (2017) - Ho Chi Minh City University of Technology",
            "publications": "5 papers in international conferences, 2 papers in journals"
        },
        {
            "email": "lecturer2@hcmute.edu.vn",
            "full_name": "ThS. Lê Văn Chính",
            "employee_id": "GV002",
            "degree": "Thạc sĩ Kỹ thuật Phần mềm",
            "title": "Thạc sĩ",
            "department": "Bộ môn Hệ thống Thông tin",
            "specialization": "Phát triển phần mềm, Hệ thống Cơ sở dữ liệu",
            "phone": "0987654321",
            "office_location": "A4-305",
            "research_interests": "Thiết kế mẫu, Kiến trúc phần mềm, DevOps",
            "teaching_subjects": "Cơ sở dữ liệu, Phát triển ứng dụng Web, Hệ quản trị cơ sở dữ liệu",
            "years_experience": 5,
            "qualifications": "Master of Software Engineering (2019) - University of Technology\nBachelor of IT (2017)",
            "publications": "3 papers in regional conferences, Industry certifications"
        },
        {
            "email": "lecturer3@hcmute.edu.vn",
            "full_name": "Ks. Phạm Thị Linh",
            "employee_id": "GV003",
            "degree": "Thạc sĩ Công nghệ Thông tin",
            "title": "Thạc sĩ",
            "department": "Bộ môn Công nghệ Web",
            "specialization": "Web Development, Mobile Application",
            "phone": "0912345678",
            "office_location": "A4-310",
            "research_interests": "Frontend frameworks, User Experience Design, Progressive Web Apps",
            "teaching_subjects": "HTML/CSS/JavaScript, Framework Web, Thiết kế giao diện người dùng",
            "years_experience": 6,
            "qualifications": "Master of IT (2020) - Ho Chi Minh City University of Technology\nCertified Web Developer",
            "publications": "2 papers in local conferences, Multiple project case studies"
        }
    ]
    
    created_lecturers = []
    for lec_data in lecturers_data:
        existing = db.query(User).filter(User.email == lec_data["email"]).first()
        if not existing:
            lecturer = User(
                **lec_data,
                role="lecturer",
                hashed_password=get_password_hash("lecturer123"),
                is_active=True
            )
            db.add(lecturer)
            db.flush()
            created_lecturers.append(lecturer)
            print(f"  ✓ Created lecturer: {lec_data['full_name']}")
        else:
            created_lecturers.append(existing)
            print(f"  ⚠ Lecturer already exists: {lec_data['email']}")
    
    db.commit()
    return created_lecturers

def create_comprehensive_syllabuses(db: Session, lecturers: list):
    """Create comprehensive demo syllabuses for each lecturer"""
    print("\n📖 Creating Comprehensive Syllabuses...")
    
    base_syllabuses_data = [
        # For lecturer 1 - AI/ML focused
        {
            "lecturer_idx": 0,
            "subject_code": "IT101",
            "subject_name": "Nhập môn Lập trình Python",
            "credits": 4,
            "semester": 1,
            "department": "Bộ môn Khoa học Máy tính",
            "academic_year": "2024-2025",
            "status": "published",
            "objectives": "Học viên nắm vững kiến thức cơ bản về lập trình Python, các cấu trúc dữ liệu, và quy trình viết mã sạch.",
            "content": "Python syntax, Data types, Control flow, Functions, OOP basics",
            "teaching_methods": "Giảng dạy trên lớp, Lab thực hành, Dự án nhóm",
            "assessment_methods": "Bài tập: 20%, Project: 30%, Thi giữa kỳ: 20%, Thi cuối kỳ: 30%",
            "textbooks": [
                {"title": "Python Crash Course", "author": "Eric Matthes", "year": 2023},
                {"title": "Automate the Boring Stuff with Python", "author": "Al Sweigart", "year": 2023}
            ]
        },
        {
            "lecturer_idx": 0,
            "subject_code": "IT102",
            "subject_name": "Cấu trúc Dữ liệu và Giải thuật",
            "credits": 4,
            "semester": 2,
            "department": "Bộ môn Khoa học Máy tính",
            "academic_year": "2024-2025",
            "status": "published",
            "objectives": "Hiểu và áp dụng các cấu trúc dữ liệu cơ bản và giải thuật tối ưu hóa.",
            "content": "Array, Linked List, Stack, Queue, Tree, Graph, Sorting, Searching",
            "teaching_methods": "Giảng dạy lý thuyết, Bài tập coding, Phân tích độ phức tạp",
            "assessment_methods": "Bài tập: 20%, Quiz: 20%, Project: 30%, Thi cuối kỳ: 30%",
            "textbooks": [
                {"title": "Introduction to Algorithms", "author": "Cormen et al.", "year": 2022}
            ]
        },
        {
            "lecturer_idx": 0,
            "subject_code": "IT103",
            "subject_name": "Trí tuệ Nhân tạo - Giới thiệu",
            "credits": 3,
            "semester": 3,
            "department": "Bộ môn Khoa học Máy tính",
            "academic_year": "2024-2025",
            "status": "published",
            "objectives": "Giới thiệu các khái niệm cơ bản của AI và áp dụng vào các bài toán thực tế.",
            "content": "Search algorithms, Logic, Machine Learning basics, Neural Networks intro",
            "teaching_methods": "Giảng dạy lý thuyết, Demo tương tác, Project thực hành",
            "assessment_methods": "Bài tập: 15%, Project: 40%, Thi cuối kỳ: 45%",
            "textbooks": [
                {"title": "Artificial Intelligence: A Modern Approach", "author": "Russell & Norvig", "year": 2023}
            ]
        },
        {
            "lecturer_idx": 0,
            "subject_code": "IT104",
            "subject_name": "Deep Learning và Ứng dụng",
            "credits": 3,
            "semester": 5,
            "department": "Bộ môn Khoa học Máy tính",
            "academic_year": "2024-2025",
            "status": "in_review",
            "objectives": "Nắm vững kiến thức về Deep Learning và xây dựng các mô hình neural networks.",
            "content": "CNN, RNN, LSTM, Transformers, Transfer Learning, Applications",
            "teaching_methods": "Giảng dạy lý thuyết, Lab hands-on, Dự án thực tế",
            "assessment_methods": "Bài tập: 20%, Midterm: 30%, Project: 50%",
            "textbooks": [
                {"title": "Deep Learning", "author": "Goodfellow, Bengio, Courville", "year": 2023}
            ]
        },
        
        # For lecturer 2 - Database/Systems focused
        {
            "lecturer_idx": 1,
            "subject_code": "IT201",
            "subject_name": "Cơ sở Dữ liệu Quan hệ",
            "credits": 4,
            "semester": 2,
            "department": "Bộ môn Hệ thống Thông tin",
            "academic_year": "2024-2025",
            "status": "published",
            "objectives": "Thiết kế, xây dựng và quản lý cơ sở dữ liệu quan hệ.",
            "content": "ER diagram, SQL, Normalization, Indexing, Transaction",
            "teaching_methods": "Giảng dạy lý thuyết, Demo SQL, Lab thực hành",
            "assessment_methods": "Bài tập: 20%, Quiz: 20%, Project: 30%, Thi cuối kỳ: 30%",
            "textbooks": [
                {"title": "Database System Concepts", "author": "Silberschatz et al.", "year": 2023}
            ]
        },
        {
            "lecturer_idx": 1,
            "subject_code": "IT202",
            "subject_name": "Hệ quản trị Cơ sở dữ liệu MySQL",
            "credits": 3,
            "semester": 3,
            "department": "Bộ môn Hệ thống Thông tin",
            "academic_year": "2024-2025",
            "status": "published",
            "objectives": "Sử dụng MySQL cho các ứng dụng thực tế.",
            "content": "MySQL setup, Queries, Stored Procedures, Views, Performance tuning",
            "teaching_methods": "Lab hands-on, Dự án thực tế, Case studies",
            "assessment_methods": "Bài tập: 30%, Project: 50%, Thi: 20%",
            "textbooks": [
                {"title": "MySQL Tutorial", "author": "W3Schools & MySQL Docs", "year": 2024}
            ]
        },
        {
            "lecturer_idx": 1,
            "subject_code": "IT203",
            "subject_name": "Phát triển Ứng dụng Web với PHP",
            "credits": 4,
            "semester": 3,
            "department": "Bộ môn Hệ thống Thông tin",
            "academic_year": "2024-2025",
            "status": "submitted",
            "objectives": "Xây dựng ứng dụng web hoàn chỉnh với PHP và MySQL.",
            "content": "PHP basics, OOP in PHP, Laravel framework, REST API, Security",
            "teaching_methods": "Giảng dạy lý thuyết, Lab thực hành, Project nhóm",
            "assessment_methods": "Bài tập: 20%, Midterm: 20%, Project: 50%, Thi: 10%",
            "textbooks": [
                {"title": "PHP Complete Reference", "author": "Gutmans et al.", "year": 2023}
            ]
        },
        {
            "lecturer_idx": 1,
            "subject_code": "IT204",
            "subject_name": "DevOps và Continuous Integration",
            "credits": 3,
            "semester": 5,
            "department": "Bộ môn Hệ thống Thông tin",
            "academic_year": "2024-2025",
            "status": "draft",
            "objectives": "Hiểu quy trình DevOps và CI/CD pipeline.",
            "content": "Docker, Kubernetes, Jenkins, Git, Deployment strategies",
            "teaching_methods": "Demo hands-on, Lab networking, Case studies",
            "assessment_methods": "Bài tập: 25%, Project: 50%, Presentation: 25%",
            "textbooks": [
                {"title": "The Phoenix Project", "author": "Gene Kim et al.", "year": 2023}
            ]
        },
        
        # For lecturer 3 - Web/Frontend focused
        {
            "lecturer_idx": 2,
            "subject_code": "IT301",
            "subject_name": "HTML, CSS và Responsive Design",
            "credits": 3,
            "semester": 1,
            "department": "Bộ môn Công nghệ Web",
            "academic_year": "2024-2025",
            "status": "published",
            "objectives": "Nắm vững HTML5, CSS3 và thiết kế responsive.",
            "content": "HTML structure, CSS layouts, Flexbox, Grid, Media queries, Responsive design",
            "teaching_methods": "Demo live coding, Lab thực hành, Design challenges",
            "assessment_methods": "Bài tập: 30%, Quiz: 20%, Project: 40%, Attendance: 10%",
            "textbooks": [
                {"title": "MDN Web Docs", "author": "Mozilla", "year": 2024}
            ]
        },
        {
            "lecturer_idx": 2,
            "subject_code": "IT302",
            "subject_name": "JavaScript Nâng cao",
            "credits": 4,
            "semester": 2,
            "department": "Bộ môn Công nghệ Web",
            "academic_year": "2024-2025",
            "status": "published",
            "objectives": "Thành thạo JavaScript cho phát triển web hiện đại.",
            "content": "ES6+, Async/Await, DOM manipulation, Promises, Callbacks, API calls",
            "teaching_methods": "Giảng dạy lý thuyết, Lab hands-on, Code reviews",
            "assessment_methods": "Bài tập: 25%, Midterm: 25%, Project: 40%, Participation: 10%",
            "textbooks": [
                {"title": "You Don't Know JS", "author": "Kyle Simpson", "year": 2023}
            ]
        },
        {
            "lecturer_idx": 2,
            "subject_code": "IT303",
            "subject_name": "React Framework - Xây dựng giao diện hiện đại",
            "credits": 4,
            "semester": 3,
            "department": "Bộ môn Công nghệ Web",
            "academic_year": "2024-2025",
            "status": "published",
            "objectives": "Xây dựng single-page applications với React.",
            "content": "Components, Hooks, State management, Routing, API integration, Testing",
            "teaching_methods": "Demo live coding, Lab projects, Code walkthroughs",
            "assessment_methods": "Bài tập: 20%, Quiz: 20%, Project: 50%, Code review: 10%",
            "textbooks": [
                {"title": "React Documentation & The Road to React", "author": "Facebook & Robin Wieruch", "year": 2024}
            ]
        },
        {
            "lecturer_idx": 2,
            "subject_code": "IT304",
            "subject_name": "UI/UX Design Principles",
            "credits": 3,
            "semester": 4,
            "department": "Bộ môn Công nghệ Web",
            "academic_year": "2024-2025",
            "status": "in_review",
            "objectives": "Thiết kế giao diện người dùng đẹp, thân thiện và hiệu quả.",
            "content": "Design thinking, User research, Wireframing, Prototyping, Accessibility, Color theory",
            "teaching_methods": "Giảng dạy lý thuyết, Design workshops, Portfolio presentations",
            "assessment_methods": "Assignments: 30%, Design project: 50%, Presentation: 20%",
            "textbooks": [
                {"title": "Design of Everyday Things", "author": "Don Norman", "year": 2023}
            ]
        }
    ]
    
    created_syllabuses = []
    for syl_data in base_syllabuses_data:
        lecturer_idx = syl_data.pop("lecturer_idx")
        
        existing = db.query(Syllabus).filter(
            Syllabus.subject_code == syl_data["subject_code"]
        ).first()
        
        if not existing:
            # Assign dates based on status
            now = datetime.now(UTC)
            syllabus = Syllabus(
                **syl_data,
                created_by=lecturers[lecturer_idx].id,
                created_at=now - timedelta(days=30),
                updated_at=now - timedelta(days=5)
            )
            
            if syl_data["status"] == "published":
                syllabus.is_published = True
                syllabus.published_at = now - timedelta(days=10)
            
            db.add(syllabus)
            db.flush()
            created_syllabuses.append(syllabus)
            print(f"  ✓ Created: {syl_data['subject_code']} - {syl_data['subject_name'][:40]}... (Status: {syl_data['status']})")
        else:
            created_syllabuses.append(existing)
    
    db.commit()
    return created_syllabuses

def create_reviews(db: Session, syllabuses: list, lecturers: list):
    """Create review/feedback data"""
    print("\n💬 Creating Reviews & Feedback...")
    
    # Delete existing reviews
    db.query(Review).delete()
    db.flush()
    
    reviews_data = []
    for i, syl in enumerate(syllabuses[:5]):  # Only first 5 syllabuses
        reviews_data.append({
            "syllabus_id": syl.id,
            "created_by": lecturers[(i + 1) % len(lecturers)].id,
            "section": ["objectives", "content", "assessment"][i % 3],
            "content": [
                "Giáo trình rất chi tiết, có thể thêm các ví dụ thực tế.",
                "Cấu trúc nội dung tốt, mục tiêu học tập rõ ràng.",
                "CLO mapping tương đối hoàn thiện.",
                "Cần bổ sung tài liệu tham khảo thêm.",
                "Phương pháp đánh giá rõ ràng và hợp lý."
            ][i % 5]
        })
    
    created_reviews = []
    for review_data in reviews_data:
        review = Review(
            **review_data,
            created_at=datetime.now(UTC) - timedelta(days=7),
            updated_at=datetime.now(UTC) - timedelta(days=3)
        )
        db.add(review)
        db.flush()
        created_reviews.append(review)
        print(f"  ✓ Created review for syllabus {review_data['syllabus_id']}")
    
    db.commit()
    return created_reviews

def create_notifications(db: Session, lecturers: list, syllabuses: list):
    """Create notifications"""
    print("\n🔔 Creating Notifications...")
    
    # Delete existing notifications
    db.query(Notification).delete()
    db.flush()
    
    notifications_data = [
        {
            "user_id": 0,
            "title": "Giáo trình mới được duyệt",
            "message": "Giáo trình 'Nhập môn Lập trình Python' của bạn đã được duyệt.",
            "notification_type": "approve",
            "is_read": True
        },
        {
            "user_id": 0,
            "title": "Có phản hồi mới",
            "message": "Bạn có phản hồi mới cho giáo trình 'Cấu trúc Dữ liệu'.",
            "notification_type": "update",
            "is_read": True
        },
        {
            "user_id": 0,
            "title": "Yêu cầu chỉnh sửa",
            "message": "Vui lòng chỉnh sửa giáo trình 'Deep Learning và Ứng dụng' theo nhận xét.",
            "notification_type": "reject",
            "is_read": False
        },
        {
            "user_id": 0,
            "title": "Lời mời cộng tác",
            "message": "Bạn được mời cộng tác trong dự án giáo trình mới.",
            "notification_type": "follow",
            "is_read": False
        },
        {
            "user_id": 1,
            "title": "Giáo trình được xuất bản",
            "message": "Giáo trình 'Cơ sở Dữ liệu Quan hệ' của bạn đã được xuất bản.",
            "notification_type": "approve",
            "is_read": True
        },
        {
            "user_id": 1,
            "title": "Cập nhật hệ thống",
            "message": "Có cập nhật mới trong hệ thống quản lý giáo trình.",
            "notification_type": "update",
            "is_read": False
        },
        {
            "user_id": 2,
            "title": "Phản hồi từ sinh viên",
            "message": "Sinh viên đã gửi phản hồi về giáo trình 'React Framework'.",
            "notification_type": "update",
            "is_read": True
        }
    ]
    
    created_notifications = []
    for notif_data in notifications_data:
        user_id = lecturers[notif_data.pop("user_id")].id
        
        notification = Notification(
            user_id=user_id,
            **notif_data,
            created_at=datetime.now(UTC) - timedelta(days=3)
        )
        db.add(notification)
        db.flush()
        created_notifications.append(notification)
        print(f"  ✓ Created notification: '{notif_data['title']}'")
    
    db.commit()
    return created_notifications

def create_clos_for_syllabuses(db: Session, syllabuses: list):
    """Create CLOs (Course Learning Outcomes) for syllabuses"""
    print("\n🎯 Creating Course Learning Outcomes (CLOs)...")
    
    clo_templates = [
        {
            "code": "CLO1",
            "description": "Hiểu biết kiến thức cơ bản và nắm vững các khái niệm chính của môn học.",
            "cognitive_level": "K2"
        },
        {
            "code": "CLO2",
            "description": "Áp dụng kiến thức vào giải quyết các bài toán thực tế.",
            "cognitive_level": "K3"
        },
        {
            "code": "CLO3",
            "description": "Phân tích và so sánh các phương pháp, kỹ thuật khác nhau.",
            "cognitive_level": "K4"
        },
        {
            "code": "CLO4",
            "description": "Đánh giá và đưa ra giải pháp tối ưu cho các vấn đề.",
            "cognitive_level": "K5"
        }
    ]
    
    created_clos = []
    for syl in syllabuses:
        # Delete existing CLOs to refresh
        db.query(CLO).filter(CLO.syllabus_id == syl.id).delete()
        db.flush()
        
        for i, clo_template in enumerate(clo_templates[:3]):  # Create 3 CLOs per syllabus
            clo = CLO(
                syllabus_id=syl.id,
                **clo_template,
                weight=1.0
            )
            db.add(clo)
            db.flush()
            created_clos.append(clo)
    
    db.commit()
    print(f"  ✓ Created {len(created_clos)} CLOs")
    return created_clos

def main():
    print("=" * 60)
    print("🚀 Creating Comprehensive Lecturer Web Demo Data")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Create data in order
        lecturers = create_lecturer_profiles(db)
        syllabuses = create_comprehensive_syllabuses(db, lecturers)
        clos = create_clos_for_syllabuses(db, syllabuses)
        reviews = create_reviews(db, syllabuses, lecturers)
        notifications = create_notifications(db, lecturers, syllabuses)
        
        print("\n" + "=" * 60)
        print("✅ Data Creation Summary:")
        print(f"   • Lecturers: {len(lecturers)}")
        print(f"   • Syllabuses: {len(syllabuses)}")
        print(f"   • CLOs: {len(clos)}")
        print(f"   • Reviews: {len(reviews)}")
        print(f"   • Notifications: {len(notifications)}")
        print("=" * 60)
        print("\n✨ Demo data created successfully!")
        print("\n📝 Lecturer Accounts:")
        for lec in lecturers:
            print(f"   • Email: {lec.email}")
            print(f"     Name: {lec.full_name}")
            print(f"     Password: lecturer123\n")
        
    except Exception as e:
        print(f"\n❌ Error creating data: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()

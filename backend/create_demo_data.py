"""
Script để tạo sample data vào database test và xem kết quả
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User
from app.models.syllabus import Syllabus
from app.models.clo import CLO
from app.models.plo import PLO
from app.models.clo_plo import CLO_PLO_Mapping
from app.core.security import get_password_hash

# Create database
SQLALCHEMY_DATABASE_URL = "sqlite:///./demo_clo_plo.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

print("🔨 Tạo database và tables...")

# Create users
lecturer = User(
    email="lecturer@example.com",
    full_name="Nguyễn Văn A",
    hashed_password=get_password_hash("password123"),
    role="lecturer",
    is_active=True
)
db.add(lecturer)
db.commit()
db.refresh(lecturer)
print(f"✅ Tạo lecturer: {lecturer.full_name} (ID: {lecturer.id})")

hod = User(
    email="hod@example.com",
    full_name="Trần Thị B",
    hashed_password=get_password_hash("password123"),
    role="hod",
    is_active=True
)
db.add(hod)
db.commit()
db.refresh(hod)
print(f"✅ Tạo HOD: {hod.full_name} (ID: {hod.id})")

# Create syllabus
syllabus = Syllabus(
    subject_code="CS101",
    subject_name="Lập trình căn bản",
    description="Học lập trình Python từ cơ bản đến nâng cao",
    credits=3,
    semester=1,
    department="Khoa Công nghệ thông tin",
    academic_year="2024-2025",
    created_by=lecturer.id,
    status="draft"
)
db.add(syllabus)
db.commit()
db.refresh(syllabus)
print(f"✅ Tạo syllabus: {syllabus.subject_code} - {syllabus.subject_name} (ID: {syllabus.id})")

# Create CLOs
clos_data = [
    {"code": "CLO1", "description": "Hiểu được các khái niệm cơ bản về lập trình", "cognitive_level": "K2", "weight": 0.2},
    {"code": "CLO2", "description": "Vận dụng được các cấu trúc điều khiển", "cognitive_level": "K3", "weight": 0.3},
    {"code": "CLO3", "description": "Phân tích và thiết kế thuật toán đơn giản", "cognitive_level": "K4", "weight": 0.3},
    {"code": "CLO4", "description": "Đánh giá hiệu quả của các giải pháp lập trình", "cognitive_level": "K5", "weight": 0.2},
]

clos = []
for data in clos_data:
    clo = CLO(
        syllabus_id=syllabus.id,
        code=data["code"],
        description=data["description"],
        cognitive_level=data["cognitive_level"],
        weight=data["weight"]
    )
    db.add(clo)
    db.commit()
    db.refresh(clo)
    clos.append(clo)
    print(f"✅ Tạo CLO: {clo.code} - {clo.description[:50]}...")

# Create PLOs
plos_data = [
    {"code": "PLO1", "description": "Nắm vững kiến thức nền tảng về khoa học máy tính", "program_code": "CS", "category": "Knowledge"},
    {"code": "PLO2", "description": "Kỹ năng lập trình và giải quyết vấn đề", "program_code": "CS", "category": "Skills"},
    {"code": "PLO3", "description": "Kỹ năng phân tích và thiết kế hệ thống", "program_code": "CS", "category": "Skills"},
    {"code": "PLO4", "description": "Thái độ làm việc chuyên nghiệp và đạo đức nghề nghiệp", "program_code": "CS", "category": "Attitudes"},
]

plos = []
for data in plos_data:
    plo = PLO(
        code=data["code"],
        description=data["description"],
        program_code=data["program_code"],
        category=data["category"]
    )
    db.add(plo)
    db.commit()
    db.refresh(plo)
    plos.append(plo)
    print(f"✅ Tạo PLO: {plo.code} - {plo.description[:50]}...")

# Create mappings
mappings_data = [
    {"clo_idx": 0, "plo_idx": 0, "level": "High", "score": 0.9},
    {"clo_idx": 0, "plo_idx": 1, "level": "Medium", "score": 0.6},
    {"clo_idx": 1, "plo_idx": 1, "level": "High", "score": 0.85},
    {"clo_idx": 2, "plo_idx": 2, "level": "High", "score": 0.9},
    {"clo_idx": 3, "plo_idx": 2, "level": "Medium", "score": 0.7},
    {"clo_idx": 3, "plo_idx": 3, "level": "Low", "score": 0.4},
]

for data in mappings_data:
    mapping = CLO_PLO_Mapping(
        clo_id=clos[data["clo_idx"]].id,
        plo_id=plos[data["plo_idx"]].id,
        correlation_level=data["level"],
        correlation_score=data["score"],
        ai_suggested=False
    )
    db.add(mapping)
    db.commit()
    print(f"✅ Tạo mapping: {clos[data['clo_idx']].code} ↔ {plos[data['plo_idx']].code} ({data['level']})")

db.close()

print("\n" + "="*60)
print("✨ HOÀN THÀNH! Database đã được tạo: demo_clo_plo.db")
print("="*60)

# Now read and display the data
import sqlite3

conn = sqlite3.connect('demo_clo_plo.db')
cursor = conn.cursor()

print("\n📊 THỐNG KÊ DATABASE:")
print("-" * 60)

cursor.execute('SELECT COUNT(*) FROM users')
print(f"👥 Users: {cursor.fetchone()[0]}")

cursor.execute('SELECT COUNT(*) FROM syllabuses')
print(f"📚 Syllabus: {cursor.fetchone()[0]}")

cursor.execute('SELECT COUNT(*) FROM clos')
print(f"🎯 CLO: {cursor.fetchone()[0]}")

cursor.execute('SELECT COUNT(*) FROM plos')
print(f"🎓 PLO: {cursor.fetchone()[0]}")

cursor.execute('SELECT COUNT(*) FROM clo_plo_mappings')
print(f"🔗 Mappings: {cursor.fetchone()[0]}")

print("\n📝 CHI TIẾT CLO:")
print("-" * 60)
cursor.execute('SELECT code, description, cognitive_level, weight FROM clos')
for row in cursor.fetchall():
    print(f"  {row[0]} ({row[2]}, weight={row[3]}): {row[1]}")

print("\n📝 CHI TIẾT PLO:")
print("-" * 60)
cursor.execute('SELECT code, description, category FROM plos')
for row in cursor.fetchall():
    print(f"  {row[0]} ({row[2]}): {row[1]}")

print("\n📝 CHI TIẾT MAPPING:")
print("-" * 60)
cursor.execute('''
    SELECT c.code, p.code, m.correlation_level, m.correlation_score 
    FROM clo_plo_mappings m
    JOIN clos c ON m.clo_id = c.id
    JOIN plos p ON m.plo_id = p.id
''')
for row in cursor.fetchall():
    print(f"  {row[0]} ↔ {row[1]}: {row[2]} (score: {row[3]})")

conn.close()

print("\n" + "="*60)
print("✅ Dữ liệu đã được GHI VÀO DATABASE thành công!")
print("📁 File: demo_clo_plo.db")
print("="*60)

"""
Script ghi data demo vào MySQL XAMPP VÀ GIỮ LẠI (không xóa)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User
from app.models.clo import CLO
from app.models.plo import PLO
from app.models.clo_plo import CLO_PLO_Mapping
from app.models.syllabus import Syllabus
from app.core.security import get_password_hash
import pymysql

MYSQL_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(MYSQL_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

print("="*70)
print("📝 GHI DỮ LIỆU DEMO VÀO MYSQL XAMPP (GIỮ LẠI)")
print("="*70)

# Tạo tables nếu chưa có
print("\n📋 Tạo tables...")
Base.metadata.create_all(engine)
print("✅ Done!")

db = Session()

# Tạo Users
print("\n👥 Tạo users...")
lecturer = User(
    email="demo.lecturer@example.com",
    full_name="Nguyễn Văn Demo",
    hashed_password=get_password_hash("password123"),
    role="lecturer",
    is_active=True
)
db.add(lecturer)
db.commit()
db.refresh(lecturer)
print(f"✅ Lecturer: {lecturer.full_name} (ID: {lecturer.id})")

hod = User(
    email="demo.hod@example.com",
    full_name="Trần Thị Trưởng Khoa",
    hashed_password=get_password_hash("password123"),
    role="hod",
    is_active=True
)
db.add(hod)
db.commit()
db.refresh(hod)
print(f"✅ HOD: {hod.full_name} (ID: {hod.id})")

# Tạo Syllabus
print("\n📚 Tạo syllabus...")
syllabus = Syllabus(
    subject_code="CS101",
    subject_name="Lập trình Python nâng cao",
    description="Khóa học về Python từ cơ bản đến nâng cao",
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
print(f"✅ Syllabus: {syllabus.subject_code} - {syllabus.subject_name}")

# Tạo CLOs
print("\n🎯 Tạo CLOs...")
clos_data = [
    {"code": "CLO1", "desc": "Hiểu được các khái niệm cơ bản về lập trình Python", "level": "K2", "weight": 0.2},
    {"code": "CLO2", "desc": "Vận dụng được cấu trúc dữ liệu và thuật toán", "level": "K3", "weight": 0.3},
    {"code": "CLO3", "desc": "Phân tích và thiết kế chương trình hướng đối tượng", "level": "K4", "weight": 0.3},
    {"code": "CLO4", "desc": "Đánh giá và tối ưu hóa hiệu suất chương trình", "level": "K5", "weight": 0.2},
]

clos = []
for data in clos_data:
    clo = CLO(
        syllabus_id=syllabus.id,
        code=data["code"],
        description=data["desc"],
        cognitive_level=data["level"],
        weight=data["weight"]
    )
    db.add(clo)
    db.commit()
    db.refresh(clo)
    clos.append(clo)
    print(f"✅ {clo.code} ({clo.cognitive_level}): {clo.description[:50]}...")

# Tạo PLOs
print("\n🎓 Tạo PLOs...")
plos_data = [
    {"code": "PLO1", "desc": "Kiến thức nền tảng về khoa học máy tính", "prog": "CS", "cat": "Knowledge"},
    {"code": "PLO2", "desc": "Kỹ năng lập trình và giải quyết vấn đề", "prog": "CS", "cat": "Skills"},
    {"code": "PLO3", "desc": "Kỹ năng làm việc nhóm và giao tiếp", "prog": "CS", "cat": "Skills"},
    {"code": "PLO4", "desc": "Thái độ chuyên nghiệp và đạo đức nghề nghiệp", "prog": "CS", "cat": "Attitudes"},
]

plos = []
for data in plos_data:
    plo = PLO(
        code=data["code"],
        description=data["desc"],
        program_code=data["prog"],
        category=data["cat"]
    )
    db.add(plo)
    db.commit()
    db.refresh(plo)
    plos.append(plo)
    print(f"✅ {plo.code} ({plo.category}): {plo.description[:50]}...")

# Tạo Mappings
print("\n🔗 Tạo CLO-PLO mappings...")
mappings_data = [
    {"clo": 0, "plo": 0, "level": "High", "score": 0.9},
    {"clo": 0, "plo": 1, "level": "Medium", "score": 0.6},
    {"clo": 1, "plo": 1, "level": "High", "score": 0.85},
    {"clo": 1, "plo": 2, "level": "Medium", "score": 0.7},
    {"clo": 2, "plo": 2, "level": "High", "score": 0.9},
    {"clo": 3, "plo": 3, "level": "Medium", "score": 0.75},
]

for data in mappings_data:
    mapping = CLO_PLO_Mapping(
        clo_id=clos[data["clo"]].id,
        plo_id=plos[data["plo"]].id,
        correlation_level=data["level"],
        correlation_score=data["score"],
        ai_suggested=False
    )
    db.add(mapping)
    db.commit()
    print(f"✅ {clos[data['clo']].code} ↔ {plos[data['plo']].code}: {data['level']} ({data['score']})")

db.close()

# Verify
print("\n" + "="*70)
print("🔍 KIỂM TRA DỮ LIỆU")
print("="*70)

conn = pymysql.connect(host='localhost', user='root', password='', database='syllabus_db')
cur = conn.cursor()

print("\n📊 Thống kê:")
cur.execute('SELECT COUNT(*) FROM users')
print(f"  👥 Users: {cur.fetchone()[0]}")

cur.execute('SELECT COUNT(*) FROM syllabuses')
print(f"  📚 Syllabuses: {cur.fetchone()[0]}")

cur.execute('SELECT COUNT(*) FROM clos')
print(f"  🎯 CLOs: {cur.fetchone()[0]}")

cur.execute('SELECT COUNT(*) FROM plos')
print(f"  🎓 PLOs: {cur.fetchone()[0]}")

cur.execute('SELECT COUNT(*) FROM clo_plo_mappings')
print(f"  🔗 Mappings: {cur.fetchone()[0]}")

print("\n📝 Chi tiết Users:")
cur.execute('SELECT id, email, full_name, role FROM users ORDER BY id DESC LIMIT 5')
for r in cur.fetchall():
    print(f"  - ID {r[0]}: {r[2]} ({r[1]}) - Role: {r[3]}")

print("\n📝 Chi tiết CLOs:")
cur.execute('SELECT code, description, cognitive_level FROM clos')
for r in cur.fetchall():
    print(f"  - {r[0]} ({r[2]}): {r[1][:50]}...")

print("\n📝 Chi tiết PLOs:")
cur.execute('SELECT code, description, category FROM plos')
for r in cur.fetchall():
    print(f"  - {r[0]} ({r[2]}): {r[1][:50]}...")

print("\n📝 Chi tiết Mappings:")
cur.execute('''
    SELECT c.code, p.code, m.correlation_level, m.correlation_score 
    FROM clo_plo_mappings m
    JOIN clos c ON m.clo_id = c.id
    JOIN plos p ON m.plo_id = p.id
''')
for r in cur.fetchall():
    print(f"  - {r[0]} ↔ {r[1]}: {r[2]} (score: {r[3]})")

conn.close()

print("\n" + "="*70)
print("✅ THÀNH CÔNG! DỮ LIỆU ĐÃ GHI VÀO MYSQL VÀ GIỮ LẠI!")
print("="*70)
print("\n💡 Lưu ý:")
print("  • Tests sẽ XÓA data để đảm bảo tính độc lập")
print("  • Script này GHI DATA và GIỮ LẠI")
print("  • Chạy lại script này bất cứ lúc nào để tạo data mới")
print("\n🌐 Xem trong phpMyAdmin:")
print("  http://localhost/phpmyadmin")
print("  → Database: syllabus_db")
print("="*70)

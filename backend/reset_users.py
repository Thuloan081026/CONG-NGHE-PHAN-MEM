from sqlalchemy import create_engine, text
import hashlib

engine = create_engine('mysql+pymysql://root:@localhost:3306/syllabus_db')

# Users với mật khẩu SHA256
users = [
    {
        'email': 'admin@smd.edu.vn',
        'password': 'Admin@123',
        'full_name': 'Quản trị viên',
        'role': 'admin'
    },
    {
        'email': 'lecturer@smd.edu.vn',
        'password': 'Lecturer@123',
        'full_name': 'Nguyễn Văn A',
        'role': 'lecturer'
    },
    {
        'email': 'hod@smd.edu.vn',
        'password': 'Hod@123',
        'full_name': 'Trần Thị B',
        'role': 'hod'
    },
    {
        'email': 'aa@smd.edu.vn',
        'password': 'Aa@123',
        'full_name': 'Lê Văn C',
        'role': 'aa'
    },
    {
        'email': 'student@smd.edu.vn',
        'password': 'Student@123',
        'full_name': 'Phạm Thị D',
        'role': 'student'
    }
]

with engine.connect() as conn:
    # Xóa users cũ
    conn.execute(text("DELETE FROM users"))
    conn.commit()
    
    # Thêm users mới
    for user in users:
        hashed_password = hashlib.sha256(user['password'].encode()).hexdigest()
        conn.execute(text("""
            INSERT INTO users (email, hashed_password, full_name, role, is_active) 
            VALUES (:email, :password, :full_name, :role, 1)
        """), {
            'email': user['email'],
            'password': hashed_password,
            'full_name': user['full_name'],
            'role': user['role']
        })
    
    conn.commit()
    print("✅ Đã tạo lại 5 users với mật khẩu mới!")
    
    # Verify
    result = conn.execute(text("SELECT email, role FROM users"))
    print("\n=== Users trong database ===")
    for row in result:
        print(f"  - {row[0]} ({row[1]})")

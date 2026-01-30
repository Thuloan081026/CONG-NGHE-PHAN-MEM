"""
Script để tạo database và tables trong MySQL XAMPP
Chạy script này để khởi tạo database lần đầu
"""

import mysql.connector
from mysql.connector import Error
import sys

def create_database_and_tables():
    """Tạo database và các bảng cần thiết trong MySQL XAMPP"""
    
    print("=" * 60)
    print("KHỞI TẠO DATABASE MYSQL XAMPP")
    print("=" * 60)
    print()
    
    # Kết nối đến MySQL server (không chỉ định database)
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # XAMPP mặc định không có password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            print("✅ Đã kết nối MySQL Server")
            
            # Tạo database nếu chưa có
            print("\n📦 Đang tạo database 'syllabus_db'...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS syllabus_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ Database 'syllabus_db' đã sẵn sàng")
            
            # Chọn database
            cursor.execute("USE syllabus_db")
            
            # Tạo bảng users
            print("\n👥 Đang tạo bảng 'users'...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    hashed_password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255) NOT NULL,
                    role ENUM('admin', 'lecturer', 'hod', 'aa', 'student') NOT NULL DEFAULT 'lecturer',
                    department VARCHAR(255),
                    phone VARCHAR(50),
                    is_active BOOLEAN DEFAULT TRUE,
                    is_locked BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_email (email),
                    INDEX idx_role (role)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("✅ Bảng 'users' đã tạo")
            
            # Tạo bảng syllabuses
            print("\n📚 Đang tạo bảng 'syllabuses'...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS syllabuses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    course_code VARCHAR(50) NOT NULL,
                    course_name VARCHAR(255) NOT NULL,
                    credits INT NOT NULL,
                    semester VARCHAR(50),
                    academic_year VARCHAR(50),
                    department VARCHAR(255),
                    lecturer_id INT,
                    description TEXT,
                    objectives TEXT,
                    learning_outcomes TEXT,
                    content TEXT,
                    assessment_methods TEXT,
                    reference_materials TEXT,
                    status ENUM('draft', 'pending_hod', 'pending_aa', 'approved', 'rejected') DEFAULT 'draft',
                    version INT DEFAULT 1,
                    file_path VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (lecturer_id) REFERENCES users(id) ON DELETE SET NULL,
                    INDEX idx_course_code (course_code),
                    INDEX idx_status (status),
                    INDEX idx_lecturer (lecturer_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("✅ Bảng 'syllabuses' đã tạo")
            
            # Tạo bảng reviews
            print("\n✍️ Đang tạo bảng 'reviews'...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    syllabus_id INT NOT NULL,
                    reviewer_id INT NOT NULL,
                    review_level ENUM('hod', 'aa', 'principal', 'peer') NOT NULL,
                    status ENUM('pending', 'approved', 'rejected', 'needs_revision') DEFAULT 'pending',
                    comments TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (syllabus_id) REFERENCES syllabuses(id) ON DELETE CASCADE,
                    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_syllabus (syllabus_id),
                    INDEX idx_reviewer (reviewer_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("✅ Bảng 'reviews' đã tạo")
            
            # Tạo bảng notifications
            print("\n🔔 Đang tạo bảng 'notifications'...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    notification_type VARCHAR(50),
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user (user_id),
                    INDEX idx_read (is_read)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("✅ Bảng 'notifications' đã tạo")
            
            # Tạo bảng audit_logs
            print("\n📋 Đang tạo bảng 'audit_logs'...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    action VARCHAR(100) NOT NULL,
                    entity_type VARCHAR(50),
                    entity_id INT,
                    details TEXT,
                    ip_address VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
                    INDEX idx_user (user_id),
                    INDEX idx_action (action),
                    INDEX idx_created (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("✅ Bảng 'audit_logs' đã tạo")
            
            connection.commit()
            print("\n" + "=" * 60)
            print("✅ HOÀN TẤT! Database đã được khởi tạo thành công!")
            print("=" * 60)
            print()
            print("📊 Database: syllabus_db")
            print("🏠 Host: localhost")
            print("👤 User: root")
            print("🔑 Password: (trống)")
            print("🔗 Connection: mysql+pymysql://root:@localhost:3306/syllabus_db")
            print()
            print("✨ Bước tiếp theo: Chạy script tạo users mẫu")
            print("   python create_mysql_users.py")
            print()
            
    except Error as e:
        print(f"\n❌ Lỗi: {e}")
        print("\n💡 Đảm bảo:")
        print("   1. XAMPP đã được cài đặt")
        print("   2. MySQL Service đang chạy trong XAMPP Control Panel")
        print("   3. Port 3306 không bị chặn")
        return False
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Đã đóng kết nối MySQL")
    
    return True


if __name__ == "__main__":
    print("\n🚀 Bắt đầu khởi tạo database...\n")
    success = create_database_and_tables()
    
    if success:
        print("\n✅ Thành công!")
        sys.exit(0)
    else:
        print("\n❌ Thất bại! Vui lòng kiểm tra lại.")
        sys.exit(1)

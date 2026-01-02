#!/usr/bin/env python3
"""
Script tạo database và tables trong MySQL
Chạy script này trước khi start server lần đầu
"""

import pymysql
from app.core.config import settings

def create_database():
    """Tạo database syllabus_db trong MySQL"""
    try:
        # Kết nối tới MySQL server (không chỉ định database)
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',  # Mặc định XAMPP không có password
            port=3306
        )

        with connection.cursor() as cursor:
            # Tạo database nếu chưa tồn tại
            cursor.execute("CREATE DATABASE IF NOT EXISTS syllabus_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✅ Database 'syllabus_db' created successfully!")

        connection.commit()
        connection.close()

    except pymysql.Error as e:
        print(f"❌ Error creating database: {e}")
        return False

    return True

def test_connection():
    """Test kết nối tới database"""
    try:
        from sqlalchemy import create_engine
        engine = create_engine(settings.DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up MySQL database for Syllabus Management System...")

    if create_database():
        if test_connection():
            print("\n🎉 Database setup completed!")
            print("📋 Next steps:")
            print("1. Start the FastAPI server: uvicorn app.main:app --reload")
            print("2. Tables will be created automatically on first run")
            print("3. Access API docs at: http://localhost:8000/docs")
        else:
            print("\n❌ Database connection test failed. Please check:")
            print("- XAMPP MySQL is running")
            print("- Database credentials in config.py")
            print("- MySQL port (default: 3306)")
    else:
        print("\n❌ Database creation failed. Please check:")
        print("- XAMPP is installed and running")
        print("- MySQL service is started")
        print("- Root user has permissions")
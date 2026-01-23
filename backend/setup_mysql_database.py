"""
Setup MySQL Database for SMD System on XAMPP
This script creates the database and necessary tables
"""

import pymysql
from sqlalchemy import create_engine, text

# MySQL connection settings for XAMPP
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""  # Default XAMPP has no password
DATABASE_NAME = "smd_db"

def create_database():
    """Create the database if it doesn't exist"""
    
    print("\n" + "="*80)
    print("SETTING UP MYSQL DATABASE FOR SMD SYSTEM")
    print("="*80 + "\n")
    
    try:
        # Connect to MySQL server (without database)
        print(f"📡 Connecting to MySQL at {MYSQL_HOST}:{MYSQL_PORT}...")
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        
        cursor = connection.cursor()
        print("✅ Connected to MySQL server successfully!\n")
        
        # Check if database exists
        cursor.execute(f"SHOW DATABASES LIKE '{DATABASE_NAME}'")
        result = cursor.fetchone()
        
        if result:
            print(f"⚠️  Database '{DATABASE_NAME}' already exists")
            print(f"    Dropping and recreating to ensure clean state...")
            cursor.execute(f"DROP DATABASE {DATABASE_NAME}")
            print(f"    ✅ Dropped existing database\n")
        
        # Create database
        print(f"📊 Creating database '{DATABASE_NAME}'...")
        cursor.execute(f"CREATE DATABASE {DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Database '{DATABASE_NAME}' created successfully!\n")
        
        cursor.close()
        connection.close()
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ MySQL Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_tables():
    """Create all tables using SQLAlchemy"""
    
    print("="*80)
    print("CREATING DATABASE TABLES")
    print("="*80 + "\n")
    
    try:
        # Import models
        import sys
        from pathlib import Path
        backend_path = Path(__file__).parent
        sys.path.insert(0, str(backend_path))
        
        from app.core.database import Base
        from app.models.user import User
        # Import other models if needed
        
        # Create engine
        DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DATABASE_NAME}"
        print(f"📊 Database URL: {DATABASE_URL}\n")
        
        engine = create_engine(DATABASE_URL, echo=False)
        
        # Create all tables
        print("🔨 Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        # Get all table names
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
        
        print(f"✅ Successfully created {len(tables)} table(s):")
        for table in tables:
            print(f"    - {table}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_setup():
    """Verify database setup"""
    
    print("="*80)
    print("VERIFYING DATABASE SETUP")
    print("="*80 + "\n")
    
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=DATABASE_NAME
        )
        
        cursor = connection.cursor()
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"✅ Database verification successful!")
        print(f"    Database: {DATABASE_NAME}")
        print(f"    Tables: {len(tables)}")
        print()
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    print("\n🚀 SMD System - MySQL Database Setup\n")
    
    # Check if pymysql is installed
    try:
        import pymysql
        print("✅ pymysql module found\n")
    except ImportError:
        print("❌ pymysql not installed!")
        print("   Please run: pip install pymysql")
        exit(1)
    
    print("XAMPP MySQL Configuration:")
    print(f"  Host: {MYSQL_HOST}")
    print(f"  Port: {MYSQL_PORT}")
    print(f"  User: {MYSQL_USER}")
    print(f"  Database: {DATABASE_NAME}")
    print()
    
    print("⚠️  IMPORTANT: Make sure XAMPP MySQL is running!")
    print()
    
    input("Press Enter to continue...")
    
    # Step 1: Create database
    if not create_database():
        print("\n❌ Failed to create database. Exiting...")
        exit(1)
    
    # Step 2: Create tables
    if not create_tables():
        print("\n❌ Failed to create tables. Exiting...")
        exit(1)
    
    # Step 3: Verify setup
    if not verify_setup():
        print("\n⚠️  Setup may be incomplete")
    
    print("="*80)
    print("DATABASE SETUP COMPLETED!")
    print("="*80)
    print()
    print("📋 Next steps:")
    print("  1. Run: python create_test_users_mysql.py")
    print("  2. Start backend: uvicorn app.main:app --reload")
    print("  3. Start frontend: python -m http.server 3000")
    print("  4. Login at: http://localhost:3000/index.html")
    print()
    print("✅ Setup complete!")

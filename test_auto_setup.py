"""
Test script để demo auto-initialization
Chạy script này để test khả năng tự động khởi tạo database
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.database import create_database_if_not_exists, Base, engine, initialize_demo_users

print("=" * 60)
print("🚀 Testing Auto-Initialization")
print("=" * 60)

# Step 1: Create database
print("\n📁 Step 1: Creating database...")
create_database_if_not_exists()

# Step 2: Create tables
print("\n📋 Step 2: Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ All tables created!")

# Step 3: Initialize demo users
print("\n👥 Step 3: Initializing demo users...")
initialize_demo_users()

print("\n" + "=" * 60)
print("✅ AUTO-INITIALIZATION COMPLETE!")
print("=" * 60)
print("\n📝 Test accounts:")
print("   - admin@ut.edu.vn / admin123")
print("   - lecturer@ut.edu.vn / lecturer123")
print("   - hod@ut.edu.vn / hod123")
print("   - aa@ut.edu.vn / aa123")
print("   - student@ut.edu.vn / student123")
print("   - principal@ut.edu.vn / principal123")
print("\n🌐 Access:")
print("   - Backend: http://localhost:8000")
print("   - API Docs: http://localhost:8000/docs")
print("   - Login: http://localhost:3000")
print("\n")

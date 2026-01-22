#!/usr/bin/env python3
"""Debug login issues"""
from app.core.database import SessionLocal
from app.models.user import User
from app.services.user_service import authenticate_user
from app.core.security import verify_password

db = SessionLocal()

try:
    print("👥 Checking users in database...\n")
    
    users = db.query(User).all()
    print(f"Total users: {len(users)}\n")
    
    for user in users:
        print(f"Email: {user.email}")
        print(f"  ID: {user.id}")
        print(f"  Role: {user.role}")
        print(f"  Hash: {user.hashed_password[:50]}...")
        
        # Test authentication
        auth = authenticate_user(db, user.email, user.email.split('@')[0] + '123')
        if auth:
            print(f"  ✅ Auth works with password: {user.email.split('@')[0]}123")
        else:
            print(f"  ❌ Auth failed")
        
        # Test password verification directly
        test_passwords = ["admin123", "lecturer123", "hod123", "academic123", "student123"]
        for pwd in test_passwords:
            if verify_password(pwd, user.hashed_password):
                print(f"  ✅ Password '{pwd}' is correct!")
                break
        print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

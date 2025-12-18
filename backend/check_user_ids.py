"""Check user IDs"""
from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()
try:
    # Get lecturer user
    lecturer = db.query(User).filter(User.email == "lecturer@test.com").first()
    if lecturer:
        print(f"Lecturer ID: {lecturer.id}")
        print(f"Email: {lecturer.email}")
        print(f"Role: {lecturer.role}")
    else:
        print("Lecturer not found")
        
    # Get all users
    users = db.query(User).all()
    print(f"\nTotal users: {len(users)}")
    for u in users[:10]:
        print(f"  ID {u.id}: {u.email} ({u.role})")
finally:
    db.close()

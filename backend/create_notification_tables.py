"""
Create notification tables
"""
from app.core.database import engine, Base
from app.models.notification import Notification, SyllabusFollow

print("Creating notification tables...")
Base.metadata.create_all(bind=engine)
print("✅ Notification tables created successfully!")
print("   - notifications")
print("   - syllabus_follows")

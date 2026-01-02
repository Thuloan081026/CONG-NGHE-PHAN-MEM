"""
Check if Module 7 & 8 tables exist in database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from sqlalchemy import inspect, text

def check_tables():
    """Check if all required tables exist"""
    print("\n" + "="*60)
    print("  CHECKING MODULE 7 & 8 TABLES IN XAMPP DATABASE")
    print("="*60 + "\n")
    
    inspector = inspect(engine)
    all_tables = inspector.get_table_names()
    
    # Tables needed for Module 7 & 8
    required_tables = {
        'notifications': 'Module 8 - Notification table',
        'syllabus_follows': 'Module 8 - Student follow syllabus',
        'system_settings': 'Settings management for API keys'
    }
    
    print("Checking required tables:\n")
    all_exist = True
    
    for table, description in required_tables.items():
        if table in all_tables:
            print(f"✅ {table}")
            print(f"   {description}")
            
            # Show table structure
            columns = inspector.get_columns(table)
            print(f"   Columns: {len(columns)}")
            for col in columns[:5]:  # Show first 5 columns
                print(f"     - {col['name']} ({col['type']})")
            if len(columns) > 5:
                print(f"     ... and {len(columns) - 5} more")
            print()
        else:
            print(f"❌ {table}")
            print(f"   {description}")
            print(f"   STATUS: NOT FOUND\n")
            all_exist = False
    
    # Check data in tables
    if all_exist:
        print("\n" + "="*60)
        print("  CHECKING TABLE DATA")
        print("="*60 + "\n")
        
        with engine.connect() as conn:
            # Check notifications
            result = conn.execute(text("SELECT COUNT(*) as count FROM notifications"))
            notif_count = result.fetchone()[0]
            print(f"📊 notifications: {notif_count} records")
            
            # Check syllabus_follows
            result = conn.execute(text("SELECT COUNT(*) as count FROM syllabus_follows"))
            follow_count = result.fetchone()[0]
            print(f"📊 syllabus_follows: {follow_count} records")
            
            # Check system_settings
            result = conn.execute(text("SELECT COUNT(*) as count FROM system_settings"))
            settings_count = result.fetchone()[0]
            print(f"📊 system_settings: {settings_count} records")
            
            # Show system_settings if any
            if settings_count > 0:
                result = conn.execute(text("SELECT `key`, description, is_encrypted FROM system_settings"))
                print("\n   System Settings:")
                for row in result:
                    encrypted = "🔒" if row[2] else "📝"
                    print(f"   {encrypted} {row[0]}: {row[1]}")
    
    print("\n" + "="*60)
    if all_exist:
        print("✅ ALL TABLES EXIST IN DATABASE")
        print("="*60 + "\n")
        print("Database: syllabus_db (MySQL XAMPP)")
        print("Location: localhost:3306")
        print("\n🎉 Module 7 & 8 ready to use!")
    else:
        print("⚠️  SOME TABLES MISSING")
        print("="*60 + "\n")
        print("Run these scripts to create tables:")
        print("  python create_notification_tables.py")
        print("  python create_system_settings_table.py")
    print()

if __name__ == "__main__":
    try:
        check_tables()
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        import traceback
        traceback.print_exc()

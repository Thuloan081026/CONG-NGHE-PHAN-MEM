"""
Script to create system_settings table for storing API keys and configurations
Run this script to add settings management to the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from app.models.system_setting import SystemSetting
from sqlalchemy import inspect

def create_settings_table():
    """Create system_settings table"""
    inspector = inspect(engine)
    
    if 'system_settings' in inspector.get_table_names():
        print("✅ Table 'system_settings' already exists")
        return
    
    print("📦 Creating system_settings table...")
    SystemSetting.metadata.create_all(bind=engine)
    print("✅ Table 'system_settings' created successfully!")
    print("\nTable structure:")
    print("  - id (INT PRIMARY KEY)")
    print("  - key (VARCHAR UNIQUE)")
    print("  - value (TEXT)")
    print("  - description (TEXT)")
    print("  - is_encrypted (BOOLEAN)")
    print("  - is_active (BOOLEAN)")
    print("  - created_at (TIMESTAMP)")
    print("  - updated_at (TIMESTAMP)")
    print("  - updated_by (INT)")

if __name__ == "__main__":
    create_settings_table()

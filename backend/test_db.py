#!/usr/bin/env python3
"""
Test database connection
"""

from app.core.database import engine, SessionLocal
from sqlalchemy import text

def test_db():
    print('🧪 Testing Database Connection...')
    print('=' * 50)

    try:
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f'✅ Database connection successful: {result.fetchone()}')

        # Test session
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))
        print(f'✅ Database session successful: {result.fetchone()}')
        db.close()

    except Exception as e:
        print(f'❌ Database connection failed: {e}')
        return False

    print('🎉 Database testing completed!')
    return True

if __name__ == '__main__':
    test_db()
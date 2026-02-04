"""Add lecturer profile fields to users table"""

from sqlalchemy import text
from app.core.database import engine


def upgrade():
    """Add new columns to users table"""
    with engine.connect() as conn:
        # Add employee_id
        conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS employee_id VARCHAR(50) UNIQUE AFTER email
        """))
        
        # Add academic information
        conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS degree VARCHAR(100) AFTER is_active,
            ADD COLUMN IF NOT EXISTS title VARCHAR(100) AFTER degree,
            ADD COLUMN IF NOT EXISTS department VARCHAR(255) AFTER title,
            ADD COLUMN IF NOT EXISTS specialization VARCHAR(255) AFTER department
        """))
        
        # Add contact information
        conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS phone VARCHAR(20) AFTER specialization,
            ADD COLUMN IF NOT EXISTS office_location VARCHAR(255) AFTER phone
        """))
        
        # Add research & teaching information
        conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS research_interests TEXT AFTER office_location,
            ADD COLUMN IF NOT EXISTS teaching_subjects TEXT AFTER research_interests,
            ADD COLUMN IF NOT EXISTS years_experience INT AFTER teaching_subjects,
            ADD COLUMN IF NOT EXISTS syllabus_count INT DEFAULT 0 AFTER years_experience,
            ADD COLUMN IF NOT EXISTS qualifications TEXT AFTER syllabus_count,
            ADD COLUMN IF NOT EXISTS publications TEXT AFTER qualifications
        """))
        
        conn.commit()
        print("✅ Migration completed successfully!")


def downgrade():
    """Remove columns from users table"""
    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE users 
            DROP COLUMN IF EXISTS employee_id,
            DROP COLUMN IF EXISTS degree,
            DROP COLUMN IF EXISTS title,
            DROP COLUMN IF EXISTS department,
            DROP COLUMN IF EXISTS specialization,
            DROP COLUMN IF EXISTS phone,
            DROP COLUMN IF EXISTS office_location,
            DROP COLUMN IF EXISTS research_interests,
            DROP COLUMN IF EXISTS teaching_subjects,
            DROP COLUMN IF EXISTS years_experience,
            DROP COLUMN IF EXISTS syllabus_count,
            DROP COLUMN IF EXISTS qualifications,
            DROP COLUMN IF EXISTS publications
        """))
        
        conn.commit()
        print("✅ Rollback completed successfully!")


if __name__ == "__main__":
    print("Running migration: Add lecturer profile fields...")
    upgrade()

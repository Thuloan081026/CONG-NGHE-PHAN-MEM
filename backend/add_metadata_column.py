"""
Add file_metadata column to syllabuses table
"""
from app.core.database import engine
from sqlalchemy import text

def add_metadata_column():
    with engine.connect() as conn:
        try:
            # Check if column exists
            result = conn.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'syllabuses' 
                AND COLUMN_NAME = 'file_metadata'
            """))
            
            if result.fetchone() is None:
                # Add column if it doesn't exist
                conn.execute(text("""
                    ALTER TABLE syllabuses 
                    ADD COLUMN file_metadata JSON NULL
                """))
                conn.commit()
                print("✅ Added file_metadata column to syllabuses table")
            else:
                print("✅ file_metadata column already exists")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_metadata_column()

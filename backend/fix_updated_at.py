"""Fix updated_at column to have default value"""
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='syllabus_db'
)

try:
    cursor = connection.cursor()
    
    # Alter table to set default value for updated_at
    sql = """
    ALTER TABLE syllabuses 
    MODIFY COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    """
    
    cursor.execute(sql)
    connection.commit()
    print("✓ Updated syllabuses.updated_at column to have default CURRENT_TIMESTAMP")
    
    # Update existing rows that have NULL updated_at
    sql_update = """
    UPDATE syllabuses 
    SET updated_at = created_at 
    WHERE updated_at IS NULL
    """
    cursor.execute(sql_update)
    rows_updated = cursor.rowcount
    connection.commit()
    print(f"✓ Updated {rows_updated} rows with NULL updated_at")
    
    cursor.close()
except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()

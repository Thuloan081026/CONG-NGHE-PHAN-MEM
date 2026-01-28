import pymysql
import hashlib

# Connect to database
conn = pymysql.connect(host='localhost', user='root', password='', database='syllabus_db')
cursor = conn.cursor()

# Check if principal exists
cursor.execute("SELECT id, email, role FROM users WHERE role='principal'")
row = cursor.fetchone()

if row:
    print(f"✅ Principal account already exists: {row[1]}")
else:
    print("❌ No principal account found. Creating one...")
    
    # Use SHA256 like backend does
    password = "principal123"
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Insert principal account
    cursor.execute("""
        INSERT INTO users (email, full_name, hashed_password, role, is_active)
        VALUES (%s, %s, %s, %s, %s)
    """, ("principal@edu.vn", "Principal Demo", hashed_password, "principal", 1))
    
    conn.commit()
    print("✅ Principal account created: principal@edu.vn / principal123")

cursor.close()
conn.close()

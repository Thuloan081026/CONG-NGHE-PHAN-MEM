import pymysql
import sys
sys.path.insert(0, 'D:/smd/backend')

from app.core.security import get_password_hash

# Kết nối database
conn = pymysql.connect(
    host='localhost',
    database='smd_db',
    user='root',
    password=''
)

cursor = conn.cursor()

# Hash password mới
new_password = 'st123'
new_hash = get_password_hash(new_password)

print(f"\n🔐 Đang cập nhật password cho student@ut.edu.vn...")
print(f"   Password: {new_password}")
print(f"   New hash: {new_hash[:50]}...")

# Update password trong database
cursor.execute(
    "UPDATE users SET hashed_password = %s WHERE email = %s",
    (new_hash, 'student@ut.edu.vn')
)

conn.commit()

print(f"\n✅ Đã cập nhật password thành công!")
print(f"   Affected rows: {cursor.rowcount}")

# Verify lại
cursor.execute("SELECT email, hashed_password FROM users WHERE email = 'student@ut.edu.vn'")
result = cursor.fetchone()
print(f"\n✔ Verify:")
print(f"   Email: {result[0]}")
print(f"   Hash: {result[1][:50]}...")

cursor.close()
conn.close()

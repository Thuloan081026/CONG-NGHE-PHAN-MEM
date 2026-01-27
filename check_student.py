import pymysql

conn = pymysql.connect(host='localhost', user='root', password='', database='syllabus_db')
cursor = conn.cursor()
cursor.execute("DESCRIBE users")
print("=== Users table structure ===")
for row in cursor:
    print(row)

# Check columns available
cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='users' AND TABLE_SCHEMA='syllabus_db'")
print("\n=== Available columns ===")
for row in cursor:
    print(row[0])

# Get student data
cursor.execute("SELECT * FROM users WHERE role='student' LIMIT 1")
cols = [desc[0] for desc in cursor.description]
row = cursor.fetchone()
if row:
    print("\n=== Student user data ===")
    for col, val in zip(cols, row):
        if col == 'password_hash':
            print(f'{col}: {str(val)[:50]}...')
        else:
            print(f'{col}: {val}')

cursor.close()
conn.close()

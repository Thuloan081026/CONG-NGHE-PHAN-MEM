"""
Check database data
"""
import pymysql

# Connect to MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='syllabus_db'
)

cursor = conn.cursor()

# Check all tables
tables = [
    'users', 'syllabuses', 'clos', 'plos', 'clo_plo_mappings', 
    'reviews', 'workflow_events', 'syllabus_versions'
]

print("\nKIEM TRA DU LIEU TRONG DATABASE:")
print("="*60)

for table in tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:25} : {count:3} records")
    except Exception as e:
        print(f"{table:25} : Error - {e}")

print("="*60)

# Show sample data from users if exists
cursor.execute("SELECT id, email, role FROM users LIMIT 5")
users = cursor.fetchall()
if users:
    print("\nUSERS:")
    for u in users:
        print(f"   ID: {u[0]}, Email: {u[1]}, Role: {u[2]}")
else:
    print("\nKhong co users trong database")

# Show sample data from syllabuses if exists
cursor.execute("SELECT id, subject_code, subject_name, status FROM syllabuses LIMIT 5")
syllabuses = cursor.fetchall()
if syllabuses:
    print("\nSYLLABUSES:")
    for s in syllabuses:
        print(f"   ID: {s[0]}, Code: {s[1]}, Name: {s[2]}, Status: {s[3]}")
else:
    print("\nKhong co syllabuses trong database")

conn.close()

print("\n" + "="*60)
print("TAI SAO DATABASE TRONG?")
print("="*60)
print("""
TESTS TU DONG DON DEP DU LIEU!

Khi chay pytest, cac tests tu dong:
1. Tao du lieu test truoc moi test
2. Chay test
3. XOA SACH du lieu sau khi test xong

=> Database se TRONG sau khi chay tests!

De co du lieu production:
1. Chay app thuc te: uvicorn app.main:app
2. Hoac chay script tao sample data
""")

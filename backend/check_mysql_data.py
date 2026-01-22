import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='syllabus_db'
)
cursor = conn.cursor()

print("📊 THỐNG KÊ MYSQL DATABASE (XAMPP):")
print("="*60)

cursor.execute('SELECT COUNT(*) FROM users')
print(f"👥 Users: {cursor.fetchone()[0]}")

cursor.execute('SELECT COUNT(*) FROM syllabuses')
print(f"📚 Syllabuses: {cursor.fetchone()[0]}")

cursor.execute('SELECT COUNT(*) FROM clos')
clo_count = cursor.fetchone()[0]
print(f"🎯 CLO: {clo_count}")

cursor.execute('SELECT COUNT(*) FROM plos')
plo_count = cursor.fetchone()[0]
print(f"🎓 PLO: {plo_count}")

cursor.execute('SELECT COUNT(*) FROM clo_plo_mappings')
mapping_count = cursor.fetchone()[0]
print(f"🔗 Mappings: {mapping_count}")

if clo_count > 0:
    print("\n📝 Sample CLO data:")
    cursor.execute('SELECT code, description, cognitive_level FROM clos LIMIT 3')
    for row in cursor.fetchall():
        print(f"  - {row[0]} ({row[2]}): {row[1][:60]}...")

if plo_count > 0:
    print("\n📝 Sample PLO data:")
    cursor.execute('SELECT code, description, category FROM plos LIMIT 3')
    for row in cursor.fetchall():
        print(f"  - {row[0]} ({row[2]}): {row[1][:60]}...")

if mapping_count > 0:
    print("\n📝 Sample Mapping data:")
    cursor.execute('''
        SELECT c.code, p.code, m.correlation_level, m.correlation_score 
        FROM clo_plo_mappings m
        JOIN clos c ON m.clo_id = c.id
        JOIN plos p ON m.plo_id = p.id
        LIMIT 3
    ''')
    for row in cursor.fetchall():
        print(f"  - {row[0]} ↔ {row[1]}: {row[2]} (score: {row[3]})")

conn.close()

print("\n" + "="*60)
print("✅ Dữ liệu đã được GHI VÀO MYSQL DATABASE XAMPP!")
print("="*60)

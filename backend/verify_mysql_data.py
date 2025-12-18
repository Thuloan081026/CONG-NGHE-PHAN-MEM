import pymysql

c = pymysql.connect(host='localhost', user='root', password='', db='syllabus_db')
cur = c.cursor()

print("="*60)
print("📊 DỮ LIỆU TRONG MYSQL XAMPP")
print("="*60)

cur.execute('SELECT COUNT(*) FROM users')
print(f"\n👥 Users: {cur.fetchone()[0]}")

cur.execute('SELECT COUNT(*) FROM syllabuses')
print(f"📚 Syllabuses: {cur.fetchone()[0]}")

cur.execute('SELECT COUNT(*) FROM clos')
print(f"🎯 CLOs: {cur.fetchone()[0]}")

cur.execute('SELECT COUNT(*) FROM plos')
print(f"🎓 PLOs: {cur.fetchone()[0]}")

cur.execute('SELECT COUNT(*) FROM clo_plo_mappings')
print(f"🔗 Mappings: {cur.fetchone()[0]}")

print("\n📝 Sample CLOs:")
cur.execute('SELECT code, description FROM clos LIMIT 3')
for r in cur.fetchall():
    print(f"  - {r[0]}: {r[1][:50]}...")

print("\n📝 Sample PLOs:")
cur.execute('SELECT code, description FROM plos LIMIT 3')
for r in cur.fetchall():
    print(f"  - {r[0]}: {r[1][:50]}...")

print("\n📝 Sample Mappings:")
cur.execute('''
    SELECT c.code, p.code, m.correlation_level 
    FROM clo_plo_mappings m
    JOIN clos c ON m.clo_id = c.id
    JOIN plos p ON m.plo_id = p.id
    LIMIT 3
''')
for r in cur.fetchall():
    print(f"  - {r[0]} ↔ {r[1]}: {r[2]}")

c.close()

print("\n" + "="*60)
print("✅ THÀNH CÔNG! DỮ LIỆU ĐÃ GHI VÀO MYSQL XAMPP!")
print("="*60)
print("\n🌐 Xem trong phpMyAdmin: http://localhost/phpmyadmin")
print("   Database: syllabus_db")
print("="*60)

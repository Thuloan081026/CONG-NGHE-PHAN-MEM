import sqlite3

conn = sqlite3.connect('test_clo_plo.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("📊 Tables:", [t[0] for t in tables])
print()

# Count records in each table
cursor.execute('SELECT COUNT(*) FROM clo')
print("✅ CLO records:", cursor.fetchone()[0])

cursor.execute('SELECT COUNT(*) FROM plo')
print("✅ PLO records:", cursor.fetchone()[0])

cursor.execute('SELECT COUNT(*) FROM clo_plo_mapping')
print("✅ Mapping records:", cursor.fetchone()[0])

cursor.execute('SELECT COUNT(*) FROM users')
print("✅ Users:", cursor.fetchone()[0])

cursor.execute('SELECT COUNT(*) FROM syllabus')
print("✅ Syllabus:", cursor.fetchone()[0])
print()

# Show sample data
print("📝 Sample CLO data:")
cursor.execute('SELECT id, code, description, cognitive_level FROM clo LIMIT 3')
for row in cursor.fetchall():
    print(f"  - ID {row[0]}: {row[1]} ({row[3]}) - {row[2][:50]}...")

print("\n📝 Sample PLO data:")
cursor.execute('SELECT id, code, description FROM plo LIMIT 3')
for row in cursor.fetchall():
    print(f"  - ID {row[0]}: {row[1]} - {row[2][:50]}...")

print("\n📝 Sample Mapping data:")
cursor.execute('SELECT clo_id, plo_id, correlation_level, correlation_score FROM clo_plo_mapping LIMIT 3')
for row in cursor.fetchall():
    print(f"  - CLO {row[0]} ↔ PLO {row[1]}: {row[2]} (score: {row[3]})")

conn.close()

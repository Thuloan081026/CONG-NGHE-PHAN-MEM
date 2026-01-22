from sqlalchemy import create_engine, text

engine = create_engine('mysql+pymysql://root:@localhost:3306/syllabus_db')
conn = engine.connect()

print('=' * 60)
print('📊 DATABASE XAMPP - SUMMARY')
print('=' * 60)

# Count records
users = conn.execute(text('SELECT COUNT(*) FROM users')).fetchone()[0]
syllabuses = conn.execute(text('SELECT COUNT(*) FROM syllabuses')).fetchone()[0]
clos = conn.execute(text('SELECT COUNT(*) FROM clos')).fetchone()[0]
plos = conn.execute(text('SELECT COUNT(*) FROM plos')).fetchone()[0]
reviews = conn.execute(text('SELECT COUNT(*) FROM reviews')).fetchone()[0]

print(f'✅ Users: {users}')
print(f'✅ Syllabuses: {syllabuses}')
print(f'✅ CLOs: {clos}')
print(f'✅ PLOs: {plos}')
print(f'✅ Reviews: {reviews}')
print('=' * 60)

# Show admin accounts
print('\n📋 ADMIN ACCOUNTS:')
admins = conn.execute(text("SELECT email, full_name, role FROM users WHERE role = 'admin' LIMIT 5")).fetchall()
for a in admins:
    print(f'  • {a[1]} ({a[0]}) - Role: {a[2]}')

# Show sample syllabuses
print('\n📖 SAMPLE SYLLABUSES:')
syls = conn.execute(text('SELECT subject_code, subject_name, status FROM syllabuses LIMIT 5')).fetchall()
for s in syls:
    print(f'  • {s[0]} - {s[1]} ({s[2]})')

conn.close()
print('=' * 60)
print('✅ DATABASE READY FOR TESTING!')
print('\n🔐 LOGIN WITH:')
print('  Email: admin@hcmute.edu.vn')
print('  Password: admin123')

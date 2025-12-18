from sqlalchemy import create_engine, text

engine = create_engine('mysql+pymysql://root:@localhost:3306/syllabus_db')

with engine.connect() as conn:
    conn.execute(text('SET FOREIGN_KEY_CHECKS=0'))
    conn.execute(text('TRUNCATE TABLE clo_plo_mappings'))
    conn.execute(text('TRUNCATE TABLE clos'))
    conn.execute(text('TRUNCATE TABLE plos'))
    conn.execute(text('TRUNCATE TABLE reviews'))
    conn.execute(text('TRUNCATE TABLE syllabuses'))
    conn.execute(text('TRUNCATE TABLE users'))
    conn.execute(text('SET FOREIGN_KEY_CHECKS=1'))
    conn.commit()
    print('✅ All tables truncated successfully!')

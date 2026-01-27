#!/usr/bin/env python
# -*- coding: utf-8 -*-
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.core.security import get_password_hash

db = SessionLocal()

# Reset password cho tất cả demo users
users_to_reset = [
    ('admin@edu.vn', 'admin123'),
    ('lecturer@edu.vn', 'lecturer123'),
    ('hod@edu.vn', 'hod123'),
    ('aa@edu.vn', 'aa123'),
    ('student@edu.vn', 'student123'),
]

for email, password in users_to_reset:
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.password_hash = get_password_hash(password)
        db.commit()
        print(f'✅ Reset password {email} = {password}')
    else:
        print(f'❌ User not found: {email}')

db.close()
print('\n✨ Tất cả password đã được reset!')

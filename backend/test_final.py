#!/usr/bin/env python3
import requests

print('🎯 Final test - Ghi dữ liệu vào MySQL database...')

try:
    data = {
        'email': 'aa@university.edu.vn',
        'password': 'password123',
        'full_name': 'Lê Văn C',
        'role': 'aa'
    }
    response = requests.post('http://127.0.0.1:8000/auth/register', json=data, timeout=10)
    print(f'Status: {response.status_code}')
    print('Response:', response.text)

    if response.status_code == 200:
        print('🎉 THÀNH CÔNG! Data đã được ghi vào MySQL database!')
        print('📊 Mở phpMyAdmin để kiểm tra: http://localhost/phpmyadmin')
        print('   - Database: syllabus_db')
        print('   - Table: users')
    else:
        print('❌ Thất bại - kiểm tra server logs')

except requests.exceptions.Timeout:
    print('❌ Timeout - server có thể đã crash')
except requests.exceptions.ConnectionError:
    print('❌ Connection error - server không chạy')
except Exception as e:
    print(f'❌ Lỗi: {e}')
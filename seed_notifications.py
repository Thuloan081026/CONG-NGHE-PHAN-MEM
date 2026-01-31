"""
Seed test notifications to the database
"""
import mysql.connector
from mysql.connector import Error
from datetime import datetime

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='syllabus_db'
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # Insert test notifications for lecturer user (id=2)
        notifications = [
            {
                'user_id': 2,
                'syllabus_id': None,
                'title': 'Giáo trình đã được phê duyệt',
                'message': 'Giáo trình "Cơ sở dữ liệu nâng cao" của bạn đã được phê duyệt bởi HOD.',
                'type': 'approve',
                'is_read': 0
            },
            {
                'user_id': 2,
                'syllabus_id': None,
                'title': 'Cần sửa giáo trình',
                'message': 'Giáo trình "Trí tuệ nhân tạo" cần được sửa theo nhận xét từ HOD.',
                'type': 'reject',
                'is_read': 0
            },
            {
                'user_id': 2,
                'syllabus_id': None,
                'title': 'Cập nhật giáo trình thành công',
                'message': 'Giáo trình "Cấu trúc dữ liệu" đã được cập nhật thành công.',
                'type': 'update',
                'is_read': 1
            },
            {
                'user_id': 2,
                'syllabus_id': None,
                'title': 'Sinh viên theo dõi giáo trình của bạn',
                'message': 'Sinh viên mới đã bắt đầu theo dõi giáo trình của bạn.',
                'type': 'follow',
                'is_read': 0
            },
        ]
        
        for notif in notifications:
            sql = '''INSERT INTO notifications 
                    (user_id, syllabus_id, title, message, notification_type, is_read, created_at) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            values = (
                notif['user_id'],
                notif['syllabus_id'],
                notif['title'],
                notif['message'],
                notif['type'],
                notif['is_read'],
                datetime.utcnow()
            )
            cursor.execute(sql, values)
        
        connection.commit()
        print(f'✓ Inserted {len(notifications)} test notifications')
        
        # Verify
        cursor.execute('SELECT COUNT(*) FROM notifications WHERE user_id = 2')
        count = cursor.fetchone()[0]
        print(f'✓ Lecturer (user_id=2) now has {count} notifications')
        
        cursor.execute('SELECT id, title, notification_type, is_read FROM notifications WHERE user_id = 2')
        print('\nNotifications:')
        for row in cursor.fetchall():
            print(f'  - ID: {row[0]}, Title: {row[1]}, Type: {row[2]}, Read: {row[3]}')
        
        cursor.close()
        connection.close()
except Error as e:
    print(f'Error: {e}')

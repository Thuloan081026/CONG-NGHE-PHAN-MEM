"""
Comprehensive seed script for notifications across all users
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
        
        # Notifications for lecturer (user_id=2)
        lecturer_notifications = [
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
        
        # Notifications for student (user_id=5)
        student_notifications = [
            {
                'user_id': 5,
                'syllabus_id': None,
                'title': 'Thông báo từ giảng viên',
                'message': 'Giảng viên đã cập nhật giáo trình "Lập trình Python".',
                'type': 'update',
                'is_read': 0
            },
            {
                'user_id': 5,
                'syllabus_id': None,
                'title': 'Bài tập mới được đăng',
                'message': 'Giảng viên đã đăng bài tập mới cho khóa học "Web Development".',
                'type': 'follow',
                'is_read': 0
            },
        ]
        
        # Notifications for HOD (user_id=3)
        hod_notifications = [
            {
                'user_id': 3,
                'syllabus_id': None,
                'title': 'Có giáo trình chờ phê duyệt',
                'message': 'Có 3 giáo trình của giảng viên chờ bạn phê duyệt.',
                'type': 'approve',
                'is_read': 0
            },
        ]
        
        all_notifications = lecturer_notifications + student_notifications + hod_notifications
        
        for notif in all_notifications:
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
        print(f'✓ Inserted {len(all_notifications)} test notifications')
        
        # Verify
        cursor.execute('SELECT user_id, COUNT(*) FROM notifications GROUP BY user_id')
        print('\nNotifications by user:')
        for row in cursor.fetchall():
            user_id, count = row
            user_names = {2: 'Lecturer', 3: 'HOD', 5: 'Student'}
            print(f'  - {user_names.get(user_id, f"User {user_id}")}: {count} notifications')
        
        cursor.close()
        connection.close()
except Error as e:
    print(f'Error: {e}')

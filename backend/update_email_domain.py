import pymysql

def update_email_domains():
    try:
        connection = pymysql.connect(
            host='localhost',
            database='smd_db',
            user='root',
            password='',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        if connection:
            cursor = connection.cursor()
            
            # Kiểm tra các email có đuôi @hcmute.edu.vn
            cursor.execute("SELECT id, email, full_name, role FROM users WHERE email LIKE '%@hcmute.edu.vn'")
            users = cursor.fetchall()
            
            print("\n🔍 Tìm thấy các tài khoản có đuôi @hcmute.edu.vn:")
            print("-" * 80)
            for user in users:
                print(f"ID: {user['id']}, Email: {user['email']}, Name: {user['full_name']}, Role: {user['role']}")
            
            if users:
                print("\n📝 Đang cập nhật email domain từ @hcmute.edu.vn sang @ut.edu.vn...")
                
                # Update email domain
                cursor.execute("""
                    UPDATE users 
                    SET email = REPLACE(email, '@hcmute.edu.vn', '@ut.edu.vn')
                    WHERE email LIKE '%@hcmute.edu.vn'
                """)
                
                connection.commit()
                
                print(f"✅ Đã cập nhật {cursor.rowcount} tài khoản")
                
                # Hiển thị kết quả sau khi update
                cursor.execute("SELECT id, email, full_name, role FROM users WHERE email LIKE '%@ut.edu.vn'")
                updated_users = cursor.fetchall()
                
                print("\n✅ Danh sách tài khoản sau khi cập nhật:")
                print("-" * 80)
                for user in updated_users:
                    print(f"ID: {user['id']}, Email: {user['email']}, Name: {user['full_name']}, Role: {user['role']}")
            else:
                print("\n✅ Không tìm thấy tài khoản nào có đuôi @hcmute.edu.vn")
                
                # Hiển thị tất cả users hiện tại
                cursor.execute("SELECT id, email, full_name, role FROM users")
                all_users = cursor.fetchall()
                print("\n📋 Tất cả tài khoản trong hệ thống:")
                print("-" * 80)
                for user in all_users:
                    print(f"ID: {user['id']}, Email: {user['email']}, Name: {user['full_name']}, Role: {user['role']}")
            
            cursor.close()
            
    except Exception as e:
        print(f"❌ Lỗi kết nối MySQL: {e}")
    finally:
        if connection:
            connection.close()
            print("\n🔌 Đã đóng kết nối database")

if __name__ == "__main__":
    update_email_domains()

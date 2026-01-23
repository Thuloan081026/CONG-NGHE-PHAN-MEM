import pymysql
import bcrypt

def verify_student():
    try:
        connection = pymysql.connect(
            host='localhost',
            database='smd_db',
            user='root',
            password='',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        cursor = connection.cursor()
        
        # Kiểm tra tài khoản student
        cursor.execute("SELECT id, email, hashed_password, role FROM users WHERE email = 'student@ut.edu.vn'")
        user = cursor.fetchone()
        
        if user:
            print(f"\n✅ Tìm thấy user:")
            print(f"ID: {user['id']}")
            print(f"Email: {user['email']}")
            print(f"Role: {user['role']}")
            print(f"Password hash: {user['hashed_password'][:50]}...")
            
            # Kiểm tra password
            password = 'st123'
            password_bytes = password.encode('utf-8')
            hash_bytes = user['hashed_password'].encode('utf-8')
            
            matches = bcrypt.checkpw(password_bytes, hash_bytes)
            print(f"\n🔑 Kiểm tra password 'st123': {'✅ ĐÚNG' if matches else '❌ SAI'}")
        else:
            print("❌ Không tìm thấy user student@ut.edu.vn")
            
            # Kiểm tra email cũ
            cursor.execute("SELECT email FROM users WHERE email LIKE '%student%'")
            students = cursor.fetchall()
            if students:
                print("\n📋 Tìm thấy các tài khoản student khác:")
                for s in students:
                    print(f"  - {s['email']}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    verify_student()

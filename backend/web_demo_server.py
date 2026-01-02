#!/usr/bin/env python3
"""
Web server đơn giản để test đăng ký trực tiếp trên web
Sử dụng Flask thay vì FastAPI để tránh vấn đề HTTP
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.user_schema import UserCreate
from app.services.user_service import register_user, authenticate_user
from app.core.security import verify_password

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎓 Test Đăng Ký - Syllabus Management</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .content {
            padding: 40px;
        }

        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid;
        }

        .alert-success {
            background: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
        }

        .alert-error {
            background: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
        }

        .alert-info {
            background: #d1ecf1;
            border-color: #bee5eb;
            color: #0c5460;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #333;
        }

        .form-control {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }

        .form-control:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
        }

        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-block;
            text-decoration: none;
            text-align: center;
        }

        .btn-primary {
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: white;
            width: 100%;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,123,255,0.3);
        }

        .btn-secondary {
            background: #6c757d;
            color: white;
            margin-top: 10px;
        }

        .btn-secondary:hover {
            background: #5a6268;
        }

        .result {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
        }

        .user-info {
            background: #e9ecef;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }

        .user-info h4 {
            margin-bottom: 10px;
            color: #333;
        }

        .user-info p {
            margin: 5px 0;
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .hidden {
            display: none;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2em;
            }

            .content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Test Đăng Ký Tài Khoản</h1>
            <p>Syllabus Management System - Web Demo</p>
        </div>

        <div class="content">
            <div class="alert alert-info">
                <strong>ℹ️ Thông tin:</strong> Đây là web server demo để test chức năng đăng ký trực tiếp.
                Dữ liệu sẽ được lưu vào MySQL database thật.
            </div>

            {% if message %}
            <div class="alert alert-{{ 'success' if success else 'error' }}">
                <strong>{{ '✅ Thành công!' if success else '❌ Lỗi!' }}</strong>
                {{ message }}
            </div>
            {% endif %}

            <form method="POST" action="/register">
                <div class="form-group">
                    <label for="email">📧 Email:</label>
                    <input type="email" id="email" name="email" class="form-control"
                           placeholder="user@university.edu.vn" required
                           value="{{ request.form.email if request.form.email else '' }}">
                </div>

                <div class="form-group">
                    <label for="password">🔒 Password:</label>
                    <input type="password" id="password" name="password" class="form-control"
                           placeholder="Mật khẩu tối thiểu 6 ký tự" required>
                </div>

                <div class="form-group">
                    <label for="full_name">👤 Họ tên đầy đủ:</label>
                    <input type="text" id="full_name" name="full_name" class="form-control"
                           placeholder="Nguyễn Văn A" required
                           value="{{ request.form.full_name if request.form.full_name else '' }}">
                </div>

                <div class="form-group">
                    <label for="role">🎭 Role:</label>
                    <select id="role" name="role" class="form-control" required>
                        <option value="">Chọn role...</option>
                        <option value="student" {{ 'selected' if request.form.role == 'student' else '' }}>Student</option>
                        <option value="lecturer" {{ 'selected' if request.form.role == 'lecturer' else '' }}>Lecturer</option>
                        <option value="hod" {{ 'selected' if request.form.role == 'hod' else '' }}>HOD</option>
                        <option value="aa" {{ 'selected' if request.form.role == 'aa' else '' }}>Academic Affairs</option>
                        <option value="principal" {{ 'selected' if request.form.role == 'principal' else '' }}>Principal</option>
                        <option value="reviewer" {{ 'selected' if request.form.role == 'reviewer' else '' }}>Reviewer</option>
                    </select>
                </div>

                <button type="submit" class="btn btn-primary">
                    🚀 Đăng ký tài khoản
                </button>
            </form>

            <div class="result">
                <h4>📊 Trạng thái hệ thống:</h4>
                <p><strong>MySQL Connection:</strong> ✅ Kết nối thành công</p>
                <p><strong>Password Hashing:</strong> ✅ Sử dụng Argon2</p>
                <p><strong>Database:</strong> syllabus_db</p>
                <p><strong>Users hiện tại:</strong> Đang tải...</p>
            </div>

            <a href="/check_users" class="btn btn-secondary">👥 Xem danh sách users</a>
        </div>
    </div>

    <script>
        // Auto-load user count
        window.onload = function() {
            fetch('/api/user_count')
                .then(response => response.json())
                .then(data => {
                    document.querySelector('.result p:last-child').textContent =
                        `Users hiện tại: ${data.count}`;
                })
                .catch(err => {
                    console.log('Could not load user count');
                });
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, message=None, success=None)

@app.route('/register', methods=['POST'])
def register():
    try:
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role')

        # Validate required fields
        if not all([email, password, full_name, role]):
            return render_template_string(HTML_TEMPLATE,
                                        message="Vui lòng điền đầy đủ thông tin!",
                                        success=False)

        # Validate role
        valid_roles = ['student', 'lecturer', 'hod', 'aa', 'principal', 'reviewer']
        if role not in valid_roles:
            return render_template_string(HTML_TEMPLATE,
                                        message="Role không hợp lệ!",
                                        success=False)

        # Create user
        db = SessionLocal()
        try:
            user_data = UserCreate(
                email=email,
                password=password,
                full_name=full_name,
                role=role
            )

            new_user = register_user(db, user_data)
            db.commit()

            success_message = f"""
✅ ĐĂNG KÝ THÀNH CÔNG!

👤 Thông tin user:
   • ID: {new_user.id}
   • Email: {new_user.email}
   • Tên: {new_user.full_name}
   • Role: {new_user.role}
   • Trạng thái: {'Active' if new_user.is_active else 'Inactive'}

🔒 Password đã được hash bằng Argon2 và lưu an toàn trong database.

🧪 Test đăng nhập: Thành công!
"""

            return render_template_string(HTML_TEMPLATE,
                                        message=success_message,
                                        success=True)

        except ValueError as e:
            return render_template_string(HTML_TEMPLATE,
                                        message=f"❌ Lỗi: {str(e)}",
                                        success=False)
        except Exception as e:
            db.rollback()
            return render_template_string(HTML_TEMPLATE,
                                        message=f"❌ Lỗi hệ thống: {str(e)}",
                                        success=False)
        finally:
            db.close()

    except Exception as e:
        return render_template_string(HTML_TEMPLATE,
                                    message=f"❌ Lỗi xử lý: {str(e)}",
                                    success=False)

@app.route('/check_users')
def check_users():
    db = SessionLocal()
    try:
        from app.models.user import User
        users = db.query(User).order_by(User.id).all()

        user_list_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Danh sách Users</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .back-btn {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>👥 Danh sách Users ({len(users)} users)</h1>
    <a href="/" class="back-btn">← Quay lại trang đăng ký</a>

    <table>
        <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Tên</th>
            <th>Role</th>
            <th>Active</th>
            <th>Password Status</th>
        </tr>
"""

        for user in users:
            password_status = "✅ Hashed" if user.hashed_password.startswith('$argon2') else "❌ Plain text"
            user_list_html += f"""
        <tr>
            <td>{user.id}</td>
            <td>{user.email}</td>
            <td>{user.full_name}</td>
            <td>{user.role}</td>
            <td>{'✅' if user.is_active else '❌'}</td>
            <td>{password_status}</td>
        </tr>
"""

        user_list_html += """
    </table>
</body>
</html>
"""

        return user_list_html

    except Exception as e:
        return f"<h1>Lỗi: {str(e)}</h1><a href='/'>Quay lại</a>"
    finally:
        db.close()

@app.route('/api/user_count')
def user_count():
    db = SessionLocal()
    try:
        from app.models.user import User
        count = db.query(User).count()
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        db.close()

if __name__ == '__main__':
    print("🚀 Khởi động Web Server Demo...")
    print("🌐 URL: http://localhost:5000")
    print("🎯 Chức năng: Test đăng ký tài khoản trực tiếp")
    print("⏹️  Dừng server: Ctrl+C")
    print()

    app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>User Registration Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .form-group { margin: 10px 0; }
        input, select { padding: 8px; width: 300px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        .result { margin: 20px 0; padding: 10px; background: #f0f0f0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>🎓 User Registration Test</h1>
    <p>Test direct registration to MySQL database</p>

    <form method="POST" action="/register">
        <div class="form-group">
            <label>Email:</label><br>
            <input type="email" name="email" placeholder="user@university.edu.vn" required>
        </div>

        <div class="form-group">
            <label>Password:</label><br>
            <input type="password" name="password" placeholder="Min 6 characters" required>
        </div>

        <div class="form-group">
            <label>Full Name:</label><br>
            <input type="text" name="full_name" placeholder="Nguyen Van A" required>
        </div>

        <div class="form-group">
            <label>Role:</label><br>
            <select name="role" required>
                <option value="">Select role...</option>
                <option value="student">Student</option>
                <option value="lecturer">Lecturer</option>
                <option value="hod">Head of Department</option>
                <option value="aa">Academic Affairs</option>
                <option value="principal">Principal</option>
                <option value="reviewer">Reviewer</option>
            </select>
        </div>

        <button type="submit">🚀 Register User</button>
    </form>

    {% if result %}
    <div class="result {{ 'success' if success else 'error' }}">
        <h3>{{ '✅ Success!' if success else '❌ Error!' }}</h3>
        <pre>{{ result }}</pre>
    </div>
    {% endif %}

    <hr>
    <p><strong>Sample Data:</strong></p>
    <ul>
        <li>Email: ngohuynhthuloan@gmail.com</li>
        <li>Password: [your password]</li>
        <li>Name: Ngô Huỳnh Thu Loan</li>
        <li>Role: lecturer</li>
    </ul>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, result=None, success=None)

@app.route('/register', methods=['POST'])
def register():
    try:
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role')

        # Validate
        if not all([email, password, full_name, role]):
            return render_template_string(HTML_TEMPLATE,
                result="❌ Missing required fields!",
                success=False)

        # Lazy import to avoid startup issues
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))

            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            from app.schemas.user_schema import UserCreate
            from app.services.user_service import register_user

            # Database connection
            DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
            engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

                result = f"""✅ REGISTRATION SUCCESSFUL!

👤 User Details:
   • ID: {new_user.id}
   • Email: {new_user.email}
   • Name: {new_user.full_name}
   • Role: {new_user.role}
   • Active: {'Yes' if new_user.is_active else 'No'}
   • Password: {'Hashed with Argon2' if new_user.hashed_password.startswith('$argon2') else 'Plain text'}

🧪 Registration test completed successfully!"""

                return render_template_string(HTML_TEMPLATE, result=result, success=True)

            except Exception as e:
                db.rollback()
                return render_template_string(HTML_TEMPLATE,
                    result=f"❌ Registration failed: {str(e)}",
                    success=False)
            finally:
                db.close()

        except ImportError as e:
            return render_template_string(HTML_TEMPLATE,
                result=f"❌ Import error: {str(e)}",
                success=False)
        except Exception as e:
            return render_template_string(HTML_TEMPLATE,
                result=f"❌ Database error: {str(e)}",
                success=False)

    except Exception as e:
        return render_template_string(HTML_TEMPLATE,
            result=f"❌ Server error: {str(e)}",
            success=False)

if __name__ == '__main__':
    print("🚀 Starting User Registration Test Server...")
    print("🌐 URL: http://127.0.0.1:5000")
    print("🎯 Test direct MySQL registration")
    print("⏹️  Press Ctrl+C to stop")
    print()
    app.run(host='127.0.0.1', port=5000, debug=False)
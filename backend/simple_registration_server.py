#!/usr/bin/env python3
"""
Simple registration server - minimal version
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Registration Test</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        form { margin: 20px 0; }
        input, select { margin: 5px; padding: 8px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        .result { margin: 20px 0; padding: 10px; background: #f0f0f0; }
    </style>
</head>
<body>
    <h1>Test User Registration</h1>

    <form action="/register" method="POST">
        <div>
            <label>Email:</label><br>
            <input type="email" name="email" required>
        </div>
        <div>
            <label>Password:</label><br>
            <input type="password" name="password" required>
        </div>
        <div>
            <label>Full Name:</label><br>
            <input type="text" name="full_name" required>
        </div>
        <div>
            <label>Role:</label><br>
            <select name="role" required>
                <option value="student">Student</option>
                <option value="lecturer">Lecturer</option>
                <option value="hod">HOD</option>
            </select>
        </div>
        <button type="submit">Register</button>
    </form>

    <div class="result" id="result"></div>

    <script>
        // Simple form handling
        document.querySelector('form').addEventListener('submit', function(e) {
            document.getElementById('result').innerHTML = 'Processing...';
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/register', methods=['POST'])
def register():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role')

        if not all([email, password, full_name, role]):
            return f"""
            <h1>Registration Failed</h1>
            <p>Missing required fields</p>
            <a href="/">Back</a>
            """

        # Import here to avoid issues
        from app.schemas.user_schema import UserCreate
        from app.services.user_service import register_user

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

            result = f"""
            <h1>Registration Successful!</h1>
            <p>User ID: {new_user.id}</p>
            <p>Email: {new_user.email}</p>
            <p>Name: {new_user.full_name}</p>
            <p>Role: {new_user.role}</p>
            <p>Password hashed with Argon2: {'Yes' if new_user.hashed_password.startswith('$argon2') else 'No'}</p>
            <a href="/">Register Another User</a>
            """

        except Exception as e:
            db.rollback()
            result = f"""
            <h1>Registration Failed</h1>
            <p>Error: {str(e)}</p>
            <a href="/">Try Again</a>
            """
        finally:
            db.close()

        return result

    except Exception as e:
        return f"""
        <h1>Error</h1>
        <p>{str(e)}</p>
        <a href="/">Back</a>
        """

if __name__ == '__main__':
    print("🚀 Starting registration test server...")
    print("🌐 URL: http://localhost:5000")
    print("🎯 Simple registration form")
    app.run(debug=True, host='0.0.0.0', port=5000)
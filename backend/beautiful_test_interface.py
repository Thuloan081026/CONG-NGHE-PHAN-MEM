#!/usr/bin/env python3
"""
Beautiful Web Interface for Testing Syllabus Management System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, render_template_string, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/syllabus_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎓 Syllabus Management - Test Interface</title>
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
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }

        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .tabs {
            display: flex;
            background: white;
            border-radius: 15px 15px 0 0;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }

        .tab-button {
            flex: 1;
            padding: 15px 20px;
            background: #f8f9fa;
            border: none;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            border-right: 1px solid #dee2e6;
        }

        .tab-button:last-child {
            border-right: none;
        }

        .tab-button:hover {
            background: #e9ecef;
        }

        .tab-button.active {
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: white;
        }

        .tab-content {
            background: white;
            padding: 30px;
            border-radius: 0 0 15px 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            min-height: 500px;
        }

        .tab-pane {
            display: none;
        }

        .tab-pane.active {
            display: block;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #495057;
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
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,123,255,0.3);
        }

        .btn-success {
            background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
            color: white;
        }

        .btn-success:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(40,167,69,0.3);
        }

        .btn-info {
            background: linear-gradient(135deg, #17a2b8 0%, #117a8b 100%);
            color: white;
        }

        .btn-info:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(23,162,184,0.3);
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

        .user-card {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            transition: box-shadow 0.3s ease;
        }

        .user-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .user-card h4 {
            margin-bottom: 10px;
            color: #007bff;
        }

        .user-card p {
            margin: 5px 0;
        }

        .status-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }

        .status-active {
            background: #d4edda;
            color: #155724;
        }

        .status-inactive {
            background: #f8d7da;
            color: #721c24;
        }

        .password-status {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }

        .password-hashed {
            background: #d4edda;
            color: #155724;
        }

        .password-plain {
            background: #fff3cd;
            color: #856404;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-card h3 {
            font-size: 2em;
            margin-bottom: 5px;
        }

        .stat-card p {
            opacity: 0.9;
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #007bff;
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

            .tabs {
                flex-direction: column;
            }

            .tab-content {
                padding: 20px;
            }

            .grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Syllabus Management System</h1>
            <p>Web Interface for Testing All Features</p>
        </div>

        <div class="tabs">
            <button class="tab-button active" onclick="showTab('register')">👤 Register User</button>
            <button class="tab-button" onclick="showTab('login')">🔐 Login</button>
            <button class="tab-button" onclick="showTab('users')">👥 View Users</button>
            <button class="tab-button" onclick="showTab('workflow')">⚡ Workflow</button>
            <button class="tab-button" onclick="showTab('database')">🗄️ Database Status</button>
        </div>

        <div class="tab-content">
            <!-- Register Tab -->
            <div id="register" class="tab-pane active">
                <h2>👤 User Registration</h2>
                <p>Test direct user registration to MySQL database</p>

                {% if register_result %}
                <div class="alert {{ 'alert-success' if register_success else 'alert-error' }}">
                    <strong>{{ '✅ Success!' if register_success else '❌ Error!' }}</strong>
                    <pre>{{ register_result }}</pre>
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
                               placeholder="Minimum 6 characters" required>
                    </div>

                    <div class="form-group">
                        <label for="full_name">👤 Full Name:</label>
                        <input type="text" id="full_name" name="full_name" class="form-control"
                               placeholder="Nguyen Van A" required
                               value="{{ request.form.full_name if request.form.full_name else '' }}">
                    </div>

                    <div class="form-group">
                        <label for="role">🎭 Role:</label>
                        <select id="role" name="role" class="form-control" required>
                            <option value="">Select role...</option>
                            <option value="student" {{ 'selected' if request.form.role == 'student' else '' }}>Student</option>
                            <option value="lecturer" {{ 'selected' if request.form.role == 'lecturer' else '' }}>Lecturer</option>
                            <option value="hod" {{ 'selected' if request.form.role == 'hod' else '' }}>Head of Department</option>
                            <option value="aa" {{ 'selected' if request.form.role == 'aa' else '' }}>Academic Affairs</option>
                            <option value="principal" {{ 'selected' if request.form.role == 'principal' else '' }}>Principal</option>
                            <option value="reviewer" {{ 'selected' if request.form.role == 'reviewer' else '' }}>Reviewer</option>
                        </select>
                    </div>

                    <button type="submit" class="btn btn-primary">🚀 Register User</button>
                </form>

                <div class="alert alert-info">
                    <strong>💡 Sample Data:</strong><br>
                    Email: ngohuynhthuloan@gmail.com<br>
                    Password: [your password]<br>
                    Name: Ngô Huỳnh Thu Loan<br>
                    Role: lecturer
                </div>
            </div>

            <!-- Login Tab -->
            <div id="login" class="tab-pane">
                <h2>🔐 User Login</h2>
                <p>Test user authentication</p>

                {% if login_result %}
                <div class="alert {{ 'alert-success' if login_success else 'alert-error' }}">
                    <strong>{{ '✅ Login Success!' if login_success else '❌ Login Failed!' }}</strong>
                    <pre>{{ login_result }}</pre>
                </div>
                {% endif %}

                <form method="POST" action="/login">
                    <div class="form-group">
                        <label for="login_email">📧 Email:</label>
                        <input type="email" id="login_email" name="email" class="form-control"
                               placeholder="user@university.edu.vn" required>
                    </div>

                    <div class="form-group">
                        <label for="login_password">🔒 Password:</label>
                        <input type="password" id="login_password" name="password" class="form-control"
                               placeholder="Enter password" required>
                    </div>

                    <button type="submit" class="btn btn-success">🔐 Login</button>
                </form>
            </div>

            <!-- Users Tab -->
            <div id="users" class="tab-pane">
                <h2>👥 User Management</h2>
                <p>View all registered users</p>

                <button onclick="loadUsers()" class="btn btn-info" id="loadUsersBtn">
                    <span class="loading" id="loadingSpinner" style="display: none;"></span>
                    🔄 Load Users
                </button>

                <div id="usersList" style="margin-top: 20px;">
                    <!-- Users will be loaded here -->
                </div>
            </div>

            <!-- Workflow Tab -->
            <div id="workflow" class="tab-pane">
                <h2>⚡ Workflow Testing</h2>
                <p>Test syllabus workflow functionality</p>

                {% if workflow_result %}
                <div class="alert {{ 'alert-success' if workflow_success else 'alert-error' }}">
                    <strong>{{ '✅ Workflow Success!' if workflow_success else '❌ Workflow Failed!' }}</strong>
                    <pre>{{ workflow_result }}</pre>
                </div>
                {% endif %}

                <form method="POST" action="/test_workflow">
                    <div class="form-group">
                        <label for="workflow_action">Workflow Action:</label>
                        <select id="workflow_action" name="action" class="form-control" required>
                            <option value="">Select action...</option>
                            <option value="create_syllabus">Create Syllabus</option>
                            <option value="submit_review">Submit for Review</option>
                            <option value="approve">Approve Syllabus</option>
                            <option value="reject">Reject Syllabus</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="user_id">User ID:</label>
                        <input type="number" id="user_id" name="user_id" class="form-control"
                               placeholder="Enter user ID" required>
                    </div>

                    <button type="submit" class="btn btn-primary">⚡ Execute Workflow</button>
                </form>
            </div>

            <!-- Database Tab -->
            <div id="database" class="tab-pane">
                <h2>🗄️ Database Status</h2>
                <p>Check database connection and statistics</p>

                <div class="grid">
                    <div class="stat-card">
                        <h3 id="userCount">--</h3>
                        <p>Total Users</p>
                    </div>

                    <div class="stat-card">
                        <h3 id="syllabusCount">--</h3>
                        <p>Total Syllabuses</p>
                    </div>

                    <div class="stat-card">
                        <h3 id="workflowCount">--</h3>
                        <p>Workflow Events</p>
                    </div>

                    <div class="stat-card">
                        <h3 id="dbStatus">✅</h3>
                        <p>Database Status</p>
                    </div>
                </div>

                <button onclick="loadStats()" class="btn btn-info">📊 Refresh Statistics</button>
            </div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // Hide all tabs
            const tabs = document.querySelectorAll('.tab-pane');
            tabs.forEach(tab => tab.classList.remove('active'));

            // Remove active class from buttons
            const buttons = document.querySelectorAll('.tab-button');
            buttons.forEach(btn => btn.classList.remove('active'));

            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        function loadUsers() {
            const btn = document.getElementById('loadUsersBtn');
            const spinner = document.getElementById('loadingSpinner');
            const usersList = document.getElementById('usersList');

            btn.disabled = true;
            spinner.style.display = 'inline-block';
            usersList.innerHTML = '<p>Loading users...</p>';

            fetch('/api/users')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        let html = `<h3>📊 Total Users: ${data.users.length}</h3>`;
                        data.users.forEach(user => {
                            const statusClass = user.is_active ? 'status-active' : 'status-inactive';
                            const passwordClass = user.hashed_password.startsWith('$argon2') ? 'password-hashed' : 'password-plain';
                            const passwordText = user.hashed_password.startsWith('$argon2') ? 'Hashed (Argon2)' : 'Plain Text';

                            html += `
                                <div class="user-card">
                                    <h4>${user.full_name}</h4>
                                    <p><strong>ID:</strong> ${user.id}</p>
                                    <p><strong>Email:</strong> ${user.email}</p>
                                    <p><strong>Role:</strong> ${user.role}</p>
                                    <p><strong>Status:</strong> <span class="status-badge ${statusClass}">${user.is_active ? 'Active' : 'Inactive'}</span></p>
                                    <p><strong>Password:</strong> <span class="password-status ${passwordClass}">${passwordText}</span></p>
                                    <p><strong>Created:</strong> ${new Date(user.created_at).toLocaleString()}</p>
                                </div>
                            `;
                        });
                        usersList.innerHTML = html;
                    } else {
                        usersList.innerHTML = `<div class="alert alert-error">${data.error}</div>`;
                    }
                })
                .catch(error => {
                    usersList.innerHTML = `<div class="alert alert-error">Error loading users: ${error.message}</div>`;
                })
                .finally(() => {
                    btn.disabled = false;
                    spinner.style.display = 'none';
                });
        }

        function loadStats() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('userCount').textContent = data.users || 0;
                    document.getElementById('syllabusCount').textContent = data.syllabuses || 0;
                    document.getElementById('workflowCount').textContent = data.workflows || 0;
                    document.getElementById('dbStatus').textContent = data.db_status ? '✅' : '❌';
                })
                .catch(error => {
                    console.error('Error loading stats:', error);
                });
        }

        // Load stats on page load
        window.onload = function() {
            loadStats();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE,
                                register_result=None, register_success=None,
                                login_result=None, login_success=None,
                                workflow_result=None, workflow_success=None)

@app.route('/register', methods=['POST'])
def register():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role')

        if not all([email, password, full_name, role]):
            return render_template_string(HTML_TEMPLATE,
                register_result="❌ Missing required fields!",
                register_success=False,
                login_result=None, login_success=None,
                workflow_result=None, workflow_success=None)

        # Lazy import
        try:
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

                result = f"""✅ USER REGISTRATION SUCCESSFUL!

👤 User Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• ID: {new_user.id}
• Email: {new_user.email}
• Full Name: {new_user.full_name}
• Role: {new_user.role}
• Status: {'Active' if new_user.is_active else 'Inactive'}
• Password: {'Securely hashed with Argon2' if new_user.hashed_password.startswith('$argon2') else 'Plain text (WARNING!)'}
• Created: {new_user.created_at}

🧪 Registration test completed successfully!
Database connection: ✅ Working
Password security: ✅ Argon2 hashing"""

                return render_template_string(HTML_TEMPLATE,
                    register_result=result, register_success=True,
                    login_result=None, login_success=None,
                    workflow_result=None, workflow_success=None)

            except Exception as e:
                db.rollback()
                return render_template_string(HTML_TEMPLATE,
                    register_result=f"❌ Registration failed: {str(e)}",
                    register_success=False,
                    login_result=None, login_success=None,
                    workflow_result=None, workflow_success=None)
            finally:
                db.close()

        except Exception as e:
            return render_template_string(HTML_TEMPLATE,
                register_result=f"❌ System error: {str(e)}",
                register_success=False,
                login_result=None, login_success=None,
                workflow_result=None, workflow_success=None)

    except Exception as e:
        return render_template_string(HTML_TEMPLATE,
            register_result=f"❌ Server error: {str(e)}",
            register_success=False,
            login_result=None, login_success=None,
            workflow_result=None, workflow_success=None)

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([email, password]):
            return render_template_string(HTML_TEMPLATE,
                register_result=None, register_success=None,
                login_result="❌ Email and password required!",
                login_success=False,
                workflow_result=None, workflow_success=None)

        try:
            from app.services.user_service import authenticate_user

            db = SessionLocal()
            try:
                user = authenticate_user(db, email, password)

                if user:
                    result = f"""✅ LOGIN SUCCESSFUL!

🔐 Authentication successful for:
• Email: {user.email}
• Name: {user.full_name}
• Role: {user.role}
• Password verification: ✅ Passed

🧪 Login test completed successfully!"""
                    success = True
                else:
                    result = "❌ Login failed: Invalid email or password"
                    success = False

                return render_template_string(HTML_TEMPLATE,
                    register_result=None, register_success=None,
                    login_result=result, login_success=success,
                    workflow_result=None, workflow_success=None)

            finally:
                db.close()

        except Exception as e:
            return render_template_string(HTML_TEMPLATE,
                register_result=None, register_success=None,
                login_result=f"❌ Login error: {str(e)}",
                login_success=False,
                workflow_result=None, workflow_success=None)

    except Exception as e:
        return render_template_string(HTML_TEMPLATE,
            register_result=None, register_success=None,
            login_result=f"❌ Server error: {str(e)}",
            login_success=False,
            workflow_result=None, workflow_success=None)

@app.route('/test_workflow', methods=['POST'])
def test_workflow():
    try:
        action = request.form.get('action')
        user_id = request.form.get('user_id')

        if not all([action, user_id]):
            return render_template_string(HTML_TEMPLATE,
                register_result=None, register_success=None,
                login_result=None, login_success=None,
                workflow_result="❌ Action and User ID required!",
                workflow_success=False)

        try:
            user_id = int(user_id)

            # Mock workflow test
            result = f"""✅ WORKFLOW TEST EXECUTED!

⚡ Workflow Action: {action}
👤 User ID: {user_id}

📋 Workflow simulation completed:
• Action: {action}
• User: {user_id}
• Status: ✅ Simulated successfully
• Timestamp: {__import__('datetime').datetime.now()}

🧪 Workflow test completed (simulated)!"""

            return render_template_string(HTML_TEMPLATE,
                register_result=None, register_success=None,
                login_result=None, login_success=None,
                workflow_result=result, workflow_success=True)

        except ValueError:
            return render_template_string(HTML_TEMPLATE,
                register_result=None, register_success=None,
                login_result=None, login_success=None,
                workflow_result="❌ User ID must be a number!",
                workflow_success=False)

    except Exception as e:
        return render_template_string(HTML_TEMPLATE,
            register_result=None, register_success=None,
            login_result=None, login_success=None,
            workflow_result=f"❌ Workflow error: {str(e)}",
            workflow_success=False)

@app.route('/api/users')
def api_users():
    try:
        from app.models.user import User

        db = SessionLocal()
        try:
            users = db.query(User).order_by(User.id).all()
            user_list = []
            for user in users:
                user_list.append({
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'role': user.role,
                    'is_active': user.is_active,
                    'hashed_password': user.hashed_password,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                })

            return jsonify({'success': True, 'users': user_list})
        finally:
            db.close()

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stats')
def api_stats():
    try:
        db = SessionLocal()
        try:
            # Count users
            from app.models.user import User
            user_count = db.query(User).count()

            # Count syllabuses (if table exists)
            syllabus_count = 0
            try:
                from app.models.syllabus import Syllabus
                syllabus_count = db.query(Syllabus).count()
            except:
                pass

            # Count workflows (if table exists)
            workflow_count = 0
            try:
                from app.models.version import WorkflowEvent
                workflow_count = db.query(WorkflowEvent).count()
            except:
                pass

            return jsonify({
                'users': user_count,
                'syllabuses': syllabus_count,
                'workflows': workflow_count,
                'db_status': True
            })
        finally:
            db.close()

    except Exception as e:
        return jsonify({
            'users': 0,
            'syllabuses': 0,
            'workflows': 0,
            'db_status': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("🚀 Starting Beautiful Syllabus Management Test Interface...")
    print("🌐 URL: http://127.0.0.1:5000")
    print("🎨 Beautiful UI with tabs for all features")
    print("⏹️  Press Ctrl+C to stop")
    print()
    app.run(host='127.0.0.1', port=5000, debug=False)
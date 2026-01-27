╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║          ✅ COMPLETE DEVELOPMENT ENVIRONMENT READY!                       ║
║                                                                          ║
║     One-Command Setup for Backend + Frontend + Data                      ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

🚀 QUICK START
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ONE-COMMAND SETUP (Recommended):

  .\start.ps1 -Full

This will:
  ✅ Activate virtual environment
  ✅ Create database tables
  ✅ Create test users (admin, lecturer, hod, student, reviewer)
  ✅ Start Backend API on port 8000
  ✅ Start Frontend on port 3000
  ✅ Open new windows for each service
  ✅ Everything ready to access immediately!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MENU MODE (Select what to do):

  .\start.ps1

You can choose:
  1 | Setup Database + Seed Data
  2 | Start Backend API only (port 8000)
  3 | Start Frontend only (port 3000)
  4 | Setup + Start Backend + Frontend (RECOMMENDED)
  5 | Setup Database Only
  0 | Exit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ WHAT'S INCLUDED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Updated requirements.txt
   ✓ All dependencies listed (fastapi, sqlalchemy, pydantic-settings, etc.)
   ✓ Can install with: pip install -r requirements.txt

2. Complete Setup Script (setup-complete.py)
   ✓ Creates all database tables
   ✓ Creates 5 test users:
     - Admin:    admin@smd.edu.vn / admin123
     - Lecturer: lecturer@test.com / lecturer123
     - HOD:      hod@test.com / hod123
     - Student:  student@test.com / student123
     - Reviewer: reviewer@test.com / reviewer123

3. Unified Start Script (start.ps1)
   ✓ Menu-driven or one-command mode
   ✓ Activates virtual environment
   ✓ Runs setup automatically
   ✓ Starts backend and frontend in separate windows
   ✓ Everything configured for localhost:3000 ↔ localhost:8000

4. Backend Configuration
   ✓ CORS enabled for localhost:3000
   ✓ Auto-create database on startup
   ✓ All routers configured
   ✓ UTF-8 encoding support
   ✓ Fixed pydantic-settings import

5. Frontend Ready
   ✓ Static HTML files in frontend/lecturer-web/
   ✓ Configured to call backend API at localhost:8000
   ✓ Login redirects to dashboard on success
   ✓ All assets and libraries included

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 ACCESS POINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After running .\start.ps1 -Full:

Frontend (Port 3000):
  • Home:      http://localhost:3000/home.html
  • Dashboard: http://localhost:3000/dashboard.html (after login)
  • Create:    http://localhost:3000/syllabus-create.html
  • View:      http://localhost:3000/syllabus-view.html
  • List:      http://localhost:3000/syllabus-list.html

Backend API (Port 8000):
  • API Docs:      http://localhost:8000/docs
  • ReDoc Docs:    http://localhost:8000/redoc
  • OpenAPI JSON:  http://localhost:8000/openapi.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔐 TEST CREDENTIALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All users are automatically created and ready to use:

┌─────────────┬──────────────────────┬──────────────┐
│ Role        │ Email                │ Password     │
├─────────────┼──────────────────────┼──────────────┤
│ Admin       │ admin@smd.edu.vn     │ admin123     │
│ Lecturer    │ lecturer@test.com    │ lecturer123  │
│ HOD         │ hod@test.com         │ hod123       │
│ Student     │ student@test.com     │ student123   │
│ Reviewer    │ reviewer@test.com    │ reviewer123  │
└─────────────┴──────────────────────┴──────────────┘

Recommended for testing: lecturer@test.com / lecturer123

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Run one command:
   .\start.ps1 -Full

2. Wait for setup to complete (30-60 seconds):
   - Backend starts on port 8000
   - Frontend starts on port 3000
   - Two new PowerShell windows open

3. Open browser and navigate to:
   http://localhost:3000/home.html

4. Login with:
   Email: lecturer@test.com
   Password: lecturer123

5. After login, you're on the dashboard with full access to:
   - View syllabuses
   - Create new syllabuses
   - Edit syllabuses
   - View workflows
   - And more!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 MANUAL SETUP (If needed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you prefer to run components separately:

Step 1: Activate virtual environment
  .\activate.ps1

Step 2: Install dependencies
  pip install -r backend/requirements.txt

Step 3: Setup database and users
  python setup-complete.py

Step 4a: Start Backend (in one terminal)
  cd backend
  python -m uvicorn app.main:app --reload --port 8000

Step 4b: Start Frontend (in another terminal)
  cd frontend/lecturer-web
  python -m http.server 3000

Step 5: Open browser
  http://localhost:3000/home.html

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛠️ TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ "Port 8000 already in use"
✅ Kill the process:
   netstat -ano | findstr :8000
   taskkill /PID <number> /F

❌ "Cannot connect to MySQL"
✅ Make sure MySQL is running (or use SQLite):
   Update DATABASE_URL in backend/app/core/config.py

❌ "Frontend shows blank page"
✅ Check browser console (F12) for errors
✅ Make sure backend API is running on port 8000
✅ Refresh page (Ctrl+R)

❌ "Login not working"
✅ Check that setup-complete.py ran successfully
✅ Verify user credentials in test output
✅ Check browser local storage (F12 → Application)

❌ "PowerShell script execution blocked"
✅ Already fixed! Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 FILE REFERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Main Scripts:
  • start.ps1           ← USE THIS! (Main entry point)
  • setup-complete.py   ← Database + users setup
  • activate.ps1        ← Activate venv manually
  • run.ps1             ← Run Python files with UTF-8

Configuration:
  • backend/requirements.txt           ← All dependencies
  • backend/app/core/config.py         ← Database URL, settings
  • backend/app/main.py                ← Backend API (CORS enabled)

Frontend:
  • frontend/lecturer-web/home.html    ← Landing page
  • frontend/lecturer-web/dashboard.html
  • frontend/lecturer-web/index.html   ← Login page
  • frontend/lecturer-web/src/        ← JavaScript components

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ VERIFICATION CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After running .\start.ps1 -Full:

□ Backend window opens with "Uvicorn running on http://0.0.0.0:8000"
□ Frontend window opens with "Serving HTTP on 0.0.0.0:3000"
□ Can access http://localhost:3000/home.html
□ Can login with lecturer@test.com / lecturer123
□ Dashboard loads after successful login
□ Can create new syllabus
□ Can view API docs at http://localhost:8000/docs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 TIPS & BEST PRACTICES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Keep both windows open
   Backend and Frontend must be running for full functionality

2. Auto-reload enabled
   Changes to backend Python files auto-reload instantly

3. Use VS Code for development
   All debugging configs already set up in .vscode/

4. Check browser console
   F12 → Console tab shows useful error messages

5. Clear browser cache if needed
   Ctrl+Shift+Delete to clear local storage and cookies

6. Multiple test accounts
   Create more syllabuses to test with different roles

7. Database persistence
   Data is saved in MySQL (or SQLite depending on config)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to develop? Here's what to do:

1. Run the complete setup:
   .\start.ps1 -Full

2. Open browser:
   http://localhost:3000/home.html

3. Login:
   lecturer@test.com / lecturer123

4. Explore:
   - Dashboard
   - Create syllabus
   - View data
   - Test features

5. Develop:
   - Modify files in backend/app/ or frontend/
   - Backend auto-reloads
   - Frontend: refresh page to see changes

6. Debug:
   - Use F5 in VS Code to debug backend
   - Use browser DevTools (F12) to debug frontend
   - Check terminal for error messages

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 SUPPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Documentation:
  • FINAL_SETUP.md         - Complete setup guide
  • QUICK_RUN.md           - Quick reference
  • RUN_ANY_FILE.md        - How to run Python files
  • VS_CODE_SETUP_GUIDE.md - VS Code debugging
  • ISSUES_FIXED.txt       - What was fixed

API Documentation:
  • http://localhost:8000/docs (Swagger UI)
  • http://localhost:8000/redoc (ReDoc)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Environment fully configured
✅ All dependencies installed
✅ Database with test users created
✅ Backend + Frontend connected
✅ CORS enabled for localhost:3000
✅ UTF-8 encoding fixed
✅ Ready for immediate development

ONE COMMAND TO START EVERYTHING:
  .\start.ps1 -Full

Then access:
  http://localhost:3000/home.html

Login with:
  lecturer@test.com / lecturer123

Happy Coding! 🚀

╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║  Everything is ready. Just run: .\start.ps1 -Full                        ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

# ================================
# Terminal 1 - Backend API (8000)
# ================================
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd D:\smd\backend; D:\smd\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
)

# ================================
# Terminal 2 - Frontend Login Page (3000)
# ================================
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd D:\smd\frontend; python -m http.server 3000"
)

# ================================
# Terminal 3 - Admin Dashboard (3001)
# ================================
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd D:\smd\frontend\admin-web\html; python -m http.server 3001"
)

# ================================
# Terminal 4 - Lecturer Dashboard (3002)
# ================================
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd D:\smd\frontend\lecturer-web; python -m http.server 3002"
)

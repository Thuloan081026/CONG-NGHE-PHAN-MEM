from fastapi import FastAPI

app = FastAPI(title="Simple Test API")

@app.get("/")
def root():
    return {"message": "API is working", "status": "success"}

@app.get("/test")
def test():
    return {"status": "OK", "message": "Test endpoint working"}

@app.get("/users")
def get_users():
    """Test endpoint lấy danh sách users"""
    return {
        "users": [
            {
                "id": 1,
                "name": "Nguyễn Văn An",
                "email": "lecturer@university.edu.vn",
                "role": "lecturer",
                "status": "active"
            },
            {
                "id": 2,
                "name": "Trần Thị Bình",
                "email": "hod@university.edu.vn",
                "role": "hod",
                "status": "active"
            },
            {
                "id": 3,
                "name": "Test User",
                "email": "test@example.com",
                "role": "student",
                "status": "active"
            }
        ],
        "total": 3,
        "message": "Danh sách users mẫu"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple Test API Server...")
    print("🌐 URL: http://127.0.0.1:8001")
    print("📋 Endpoints:")
    print("  GET / - Health check")
    print("  GET /test - Test endpoint")
    print("  GET /users - Lấy danh sách users")
    print("⏹️  Press Ctrl+C to stop")
    uvicorn.run(app, host="127.0.0.1", port=8001)
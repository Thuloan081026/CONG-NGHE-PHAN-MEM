#!/usr/bin/env python3
"""
Script test ghi dữ liệu vào MySQL database qua API
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    """Test các API endpoints để ghi dữ liệu"""

    print("🚀 Testing API endpoints - Ghi dữ liệu vào MySQL...")

    # 1. Tạo users với các roles khác nhau
    print("\n1. Tạo users...")

    users = [
        {"email": "lecturer@test.com", "password": "password123", "full_name": "Nguyễn Văn A", "role": "lecturer"},
        {"email": "hod@test.com", "password": "password123", "full_name": "Trần Thị B", "role": "hod"},
        {"email": "aa@test.com", "password": "password123", "full_name": "Lê Văn C", "role": "aa"},
        {"email": "principal@test.com", "password": "password123", "full_name": "Phạm Thị D", "role": "principal"}
    ]

    created_users = []
    for user_data in users:
        try:
            response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
            if response.status_code == 200:
                print(f"   ✅ Tạo user: {user_data['email']} ({user_data['role']})")
                created_users.append(response.json())
            else:
                print(f"   ❌ Lỗi tạo user {user_data['email']}: {response.text}")
        except Exception as e:
            print(f"   ❌ Connection error: {e}")
            return

    # 2. Login để lấy token
    print("\n2. Login để lấy access token...")
    login_data = {"email": "lecturer@test.com", "password": "password123"}
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            print("   ✅ Login thành công, có access token")
        else:
            print(f"   ❌ Login thất bại: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return

    # 3. Tạo syllabus
    print("\n3. Tạo syllabus...")
    syllabus_data = {
        "subject_code": "CNPM001",
        "subject_name": "Công nghệ Phần mềm",
        "description": "Môn học về phát triển phần mềm",
        "credits": 3,
        "semester": 1,
        "department": "Công nghệ Thông tin",
        "academic_year": "2025-2026",
        "objectives": "Hiểu về quy trình phát triển phần mềm",
        "content": "Agile, Scrum, Testing, CI/CD",
        "teaching_methods": "Bài giảng, Thực hành, Project",
        "assessment_methods": "Thi viết 40%, Bài tập 30%, Project 30%",
        "prerequisites": [{"id": "PROG101", "name": "Lập trình Cơ bản"}],
        "clos": [
            {"id": "CLO1", "description": "Hiểu quy trình phát triển phần mềm", "level": "K3"},
            {"id": "CLO2", "description": "Áp dụng Agile/Scrum", "level": "K4"}
        ],
        "plos": [
            {"id": "PLO1", "description": "Kỹ năng mềm", "alignment": 0.8},
            {"id": "PLO2", "description": "Kỹ năng chuyên môn", "alignment": 0.9}
        ],
        "assessment_weights": {"attendance": 10, "assignment": 30, "exam": 60}
    }

    try:
        response = requests.post(f"{BASE_URL}/syllabus/", json=syllabus_data, headers=headers)
        if response.status_code == 200:
            syllabus = response.json()
            syllabus_id = syllabus["id"]
            print(f"   ✅ Tạo syllabus thành công: {syllabus['subject_code']} (ID: {syllabus_id})")
        else:
            print(f"   ❌ Lỗi tạo syllabus: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return

    # 4. Test workflow - Submit syllabus
    print("\n4. Test workflow - Submit syllabus...")
    workflow_data = {"syllabus_id": syllabus_id, "comment": "Đề nghị duyệt giáo trình"}

    try:
        response = requests.post(f"{BASE_URL}/workflow/submit", json=workflow_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Submit thành công - Status: {result['new_status']}")
        else:
            print(f"   ❌ Lỗi submit: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")

    # 5. Login với HOD để approve
    print("\n5. HOD approve...")
    hod_login = {"email": "hod@test.com", "password": "password123"}
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=hod_login)
        if response.status_code == 200:
            hod_token = response.json()["access_token"]
            hod_headers = {"Authorization": f"Bearer {hod_token}"}

            response = requests.post(f"{BASE_URL}/workflow/hod-approve", json=workflow_data, headers=hod_headers)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ HOD approved - Status: {result['new_status']}")
            else:
                print(f"   ❌ HOD approve failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")

    # 6. AA approve
    print("\n6. AA approve...")
    aa_login = {"email": "aa@test.com", "password": "password123"}
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=aa_login)
        if response.status_code == 200:
            aa_token = response.json()["access_token"]
            aa_headers = {"Authorization": f"Bearer {aa_token}"}

            response = requests.post(f"{BASE_URL}/workflow/aa-approve", json=workflow_data, headers=aa_headers)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ AA approved - Status: {result['new_status']}")
            else:
                print(f"   ❌ AA approve failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")

    # 7. Principal final approve
    print("\n7. Principal final approve...")
    principal_login = {"email": "principal@test.com", "password": "password123"}
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=principal_login)
        if response.status_code == 200:
            principal_token = response.json()["access_token"]
            principal_headers = {"Authorization": f"Bearer {principal_token}"}

            response = requests.post(f"{BASE_URL}/workflow/final-approve", json=workflow_data, headers=principal_headers)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Principal approved - Status: {result['new_status']}, Published: {result['is_published']}")
            else:
                print(f"   ❌ Principal approve failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")

    # 8. Check workflow history
    print("\n8. Check workflow history...")
    try:
        response = requests.get(f"{BASE_URL}/workflow/{syllabus_id}/events", headers=headers)
        if response.status_code == 200:
            history = response.json()
            print(f"   ✅ Workflow history: {history['count']} events")
            for event in history['items']:
                print(f"      - {event['action']} by user {event['performed_by']} at {event['created_at']}")
        else:
            print(f"   ❌ Get history failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")

    print("\n🎉 Hoàn thành test! Dữ liệu đã được ghi vào MySQL database.")
    print("📊 Kiểm tra phpMyAdmin để xem data: http://localhost/phpmyadmin")
    print("📋 Database: syllabus_db")
    print("🔍 Tables: users, syllabuses, workflow_events")

if __name__ == "__main__":
    # Wait a bit for server to be ready
    print("⏳ Đợi server khởi động...")
    time.sleep(3)

    test_api()
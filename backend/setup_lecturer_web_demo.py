#!/usr/bin/env python3
"""
Quick Start Guide for Creating Lecturer Web Demo Data
Hướng dẫn Nhanh Tạo Dữ liệu Demo cho Lecturer Web
"""

import os
import sys
from pathlib import Path

def print_banner():
    """Print banner"""
    print("\n" + "="*70)
    print("  🎓 LECTURER WEB DEMO DATA SETUP")
    print("  Hệ thống Quản lý & Số hóa Giáo trình")
    print("="*70 + "\n")

def check_requirements():
    """Check if necessary files exist"""
    print("📋 Kiểm tra các file cần thiết...")
    
    backend_dir = Path("backend")
    required_files = [
        "backend/create_lecturer_web_data.py",
        "backend/app/core/database.py",
        "backend/app/models/user.py",
        "backend/app/models/syllabus.py",
        "backend/app/models/notification.py"
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
            print(f"  ❌ Không tìm thấy: {file}")
        else:
            print(f"  ✓ Tìm thấy: {file}")
    
    if missing:
        print(f"\n❌ Lỗi: Thiếu {len(missing)} file!")
        return False
    
    print("\n✅ Tất cả file cần thiết đã có!\n")
    return True

def run_script():
    """Run the create_lecturer_web_data.py script"""
    print("🚀 Bắt đầu tạo dữ liệu demo...\n")
    
    # Change to backend directory
    os.chdir("backend")
    
    # Run the script
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "create_lecturer_web_data.py"],
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy script: {str(e)}")
        return False

def print_next_steps():
    """Print next steps"""
    print("\n" + "="*70)
    print("  ✨ ĐÃ HOÀN THÀNH!")
    print("="*70)
    
    print("""
📝 BƯỚC TIẾP THEO:

1️⃣  Kiểm tra Backend đang chạy:
    cd backend
    python -m uvicorn app.main:app --reload --port 8000

2️⃣  Mở Frontend (ở cửa sổ terminal khác):
    http://localhost:3000/lecturer-web/dashboard.html

3️⃣  Đăng nhập với một trong các tài khoản:

    👨‍🏫 Lecturer 1 (AI/ML):
       Email: lecturer1@hcmute.edu.vn
       Password: lecturer123
       Giáo trình: 4 (3 published, 1 in review)

    👩‍🏫 Lecturer 2 (Database/Systems):
       Email: lecturer2@hcmute.edu.vn
       Password: lecturer123
       Giáo trình: 4 (2 published, 1 submitted, 1 draft)

    👩‍🏫 Lecturer 3 (Web/Frontend):
       Email: lecturer3@hcmute.edu.vn
       Password: lecturer123
       Giáo trình: 4 (3 published, 1 in review)

4️⃣  Kiểm tra các page:
    ✓ Dashboard (/dashboard.html) - Hiển thị 12 giáo trình
    ✓ Syllabus List (/syllabus-list.html) - Danh sách với filter
    ✓ Profile (/profile.html) - Thông tin giảng viên
    ✓ Notifications (/notifications.html) - 7 thông báo demo

5️⃣  Kiểm tra CSS cải thiện:
    ✓ Màu xanh dương hài hòa trên tất cả card
    ✓ Bóng (shadow) tăng cường
    ✓ Navigation text bolder (nổi bật hơn)

📊 DỮ LIỆU ĐƯỢC TẠO:
   • 3 Giảng viên (Lecturers) - với chi tiết đầy đủ
   • 12 Giáo trình (Syllabuses) - các trạng thái khác nhau
   • 36 CLOs (Course Learning Outcomes)
   • 5 Reviews & Feedback
   • 7 Notifications (mixed read/unread)

💡 TIP: Nếu muốn tạo lại dữ liệu:
   python create_lecturer_web_data.py

🔐 Tài khoản Admin (nếu cần):
   Email: admin@hcmute.edu.vn
   Password: admin123

""")
    print("="*70 + "\n")

def main():
    """Main function"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Không thể tiếp tục. Vui lòng kiểm tra các file cần thiết.")
        sys.exit(1)
    
    # Run script
    if not run_script():
        print("\n❌ Lỗi khi tạo dữ liệu. Vui lòng kiểm tra log trên.")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Đã hủy bỏ.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

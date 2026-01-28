#!/bin/bash
# Quick Start Script for Lecturer Web Demo Data
# Dễ dàng chạy script tạo dữ liệu demo

echo ""
echo "=========================================="
echo "  🎓 LECTURER WEB DEMO DATA SETUP"
echo "=========================================="
echo ""

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "❌ Không tìm thấy thư mục 'backend'"
    echo "   Vui lòng chạy script này từ thư mục gốc của dự án"
    exit 1
fi

# Change to backend directory
cd backend

echo "📋 Kiểm tra file tạo dữ liệu..."
if [ ! -f "create_lecturer_web_data.py" ]; then
    echo "❌ Không tìm thấy: create_lecturer_web_data.py"
    exit 1
fi
echo "✓ Tìm thấy: create_lecturer_web_data.py"
echo ""

# Run the script
echo "🚀 Bắt đầu tạo dữ liệu demo..."
echo ""

python create_lecturer_web_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "  ✨ HOÀN THÀNH!"
    echo "=========================================="
    echo ""
    echo "📝 BƯỚC TIẾP THEO:"
    echo ""
    echo "1️⃣  Chạy Backend (nếu chưa chạy):"
    echo "   python -m uvicorn app.main:app --reload --port 8000"
    echo ""
    echo "2️⃣  Mở Frontend:"
    echo "   http://localhost:3000/lecturer-web/dashboard.html"
    echo ""
    echo "3️⃣  Đăng nhập với:"
    echo "   • lecturer1@hcmute.edu.vn"
    echo "   • lecturer2@hcmute.edu.vn"
    echo "   • lecturer3@hcmute.edu.vn"
    echo "   Password: lecturer123"
    echo ""
    echo "✅ Dữ liệu Demo đã được tạo thành công!"
    echo ""
else
    echo ""
    echo "❌ Lỗi khi tạo dữ liệu"
    echo "   Vui lòng kiểm tra thông báo lỗi trên"
    exit 1
fi

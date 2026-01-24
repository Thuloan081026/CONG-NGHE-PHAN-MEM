# Hướng dẫn khởi động hệ thống SMD

## Cách chạy (Từ BẤT KỲ ĐÂU)

### Windows - Cách 1: Double click
Mở File Explorer → Tìm file `d:\smd\start-all.bat` → Double click vào file

### Windows - Cách 2: Từ terminal bất kỳ
```bash
d:\smd\start-all.bat
```

Hoặc:
```bash
start d:\smd\start-all.bat
```

## Kết quả
Script sẽ tự động:
1. ✅ Khởi động Backend API trên port **8000**
2. ✅ Khởi động Lecturer Frontend trên port **3000**
3. ✅ Khởi động Admin Frontend trên port **3001**
4. ✅ Tự động mở browser tại http://localhost:3000

## Truy cập hệ thống
- **Trang login chung**: http://localhost:3000
- **Admin Dashboard**: http://localhost:3001 (tự động chuyển khi admin login)
- **Backend API**: http://127.0.0.1:8000

## Tài khoản test
| Email | Password | Role |
|-------|----------|------|
| admin@smd.edu.vn | Admin@123 | Admin |
| lecturer@smd.edu.vn | Lecturer@123 | Lecturer |

## Dừng hệ thống
Đóng 3 cửa sổ terminal (SMD Backend, SMD Lecturer, SMD Admin)

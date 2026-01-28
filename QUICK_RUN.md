# 🎯 QUICK REFERENCE - Chạy File Python

Sau khi cấu hình toàn bộ, bây giờ bạn chỉ cần:

## 🚀 3 Cách Nhanh Nhất (Chọn 1 cái)

### **1️⃣ Terminal Command (Dễ nhất)**
```powershell
# Mở Terminal: Ctrl + `
python check_health.py
python backend/create_test_users.py
python .\run-any-file.ps1 -filePath "backend/create_demo_data.py"
```

### **2️⃣ VS Code Click-Play**
1. Mở file Python bất kỳ
2. Nhấn **Ctrl+F5** (hoặc F5 để debug)
3. Chọn "Python: Current File"
✨ **Done!** File chạy ngay

### **3️⃣ Nút Run Triangle**
- Mở file → Nhấn nút ▶ ở góc phải trên cùng

---

## 📋 Các Lệnh Hữu Ích

```powershell
# Chạy file tại root
python check_health.py
python create_demo_data.py
python reset_admin_password.py

# Chạy file trong backend
python backend/create_test_users.py
python backend/init_db.py

# Chạy với arguments
python backend/check_db_data.py --verbose
python check_health.py --full-report

# Terminal tự động activate venv + set PYTHONPATH
# (không cần làm gì, tự động!)
```

---

## ✨ Đã Cấu Hình Gì?

✅ **PYTHONPATH Global** - Mọi file đều có thể import từ backend
✅ **Tự động Activate venv** - Terminal tự activate khi mở
✅ **VS Code Launch Config** - F5 chạy file ngay tức thì
✅ **Helper Scripts** - `run-any-file.ps1` cho những trường hợp đặc biệt

---

## 🆚 Trước vs Sau

| | **Trước** | **Sau** |
|---|----------|--------|
| Download file mới | Fix import, cấu hình PYTHONPATH | ✓ Chạy ngay |
| Chạy bất kỳ file nào | Lỗi ModuleNotFoundError | ✓ Không lỗi |
| Terminal | Phải activate venv | ✓ Tự động |
| Import modules | Phải chỉnh path | ✓ Toàn cầu |

---

**That's it! Now go run your code! 🚀**

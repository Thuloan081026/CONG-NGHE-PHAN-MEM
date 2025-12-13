# Student Web – Phân hệ Sinh viên

## 1. Giới thiệu

Student Web là phân hệ dành cho **Sinh viên / Người dùng công khai** trong Hệ thống Quản lý và Số hóa Giáo trình (SMD – SP26SE001).

Phân hệ này cho phép sinh viên tra cứu, đọc và theo dõi syllabus của các môn học một cách thuận tiện, thống nhất và minh bạch, thay thế cho việc tìm kiếm file PDF/Word rời rạc như phương thức truyền thống.

---

## 2. Đối tượng sử dụng

* Sinh viên đang theo học tại trường
* Người dùng công khai (public user) được phép xem syllabus đã được công bố

---

## 3. Các chức năng chính

### 3.1. Tra cứu Syllabus (Search Syllabus)

* Tìm kiếm syllabus theo **mã môn học** hoặc **tên môn học**
* Hiển thị danh sách các syllabus phù hợp
* Điều hướng đến trang chi tiết syllabus

### 3.2. Xem chi tiết Syllabus (View Syllabus Detail)

* Hiển thị đầy đủ nội dung syllabus:

  * Mô tả môn học
  * Chuẩn đầu ra (CLO)
  * Hình thức đánh giá
  * Tài liệu học tập
* Hiển thị **AI Summary** (tóm tắt nội dung bằng AI)

### 3.3. Xem lộ trình học tập (Learning Roadmap)

* Hiển thị các môn học theo từng học kỳ
* Giúp sinh viên định hướng thứ tự học các môn

### 3.4. Theo dõi Syllabus (Follow Syllabus)

* Sinh viên có thể theo dõi một syllabus
* Nhận thông báo khi syllabus được cập nhật

---

## 4. Công nghệ sử dụng

### 4.1. Frontend

* HTML5
* CSS3 (student.css)
* JavaScript (student.js – xác nhận hành động cơ bản)

### 4.2. Backend

* Python
* FastAPI
* Jinja2 Template Engine

---

## 5. Cấu trúc thư mục

```
student-web/
├── routes.py
├── templates/
│   ├── roadmap.html
│   ├── search.html
│   └── syllabus.html
└── static/
    ├── css/
    │   └── student.css
    └── js/
        └── student.js
```

---

## 6. Luồng hoạt động (Workflow)

1. Sinh viên truy cập trang **Search** hoặc **Roadmap**
2. Chọn một môn học để xem chi tiết syllabus
3. Xem nội dung syllabus và AI Summary
4. Thực hiện theo dõi syllabus (nếu cần)

---

## 7. Yêu cầu phi chức năng

* Giao diện đơn giản, dễ sử dụng
* Thời gian phản hồi nhanh khi tra cứu
* Tương thích với trình duyệt phổ biến (Chrome, Edge)
* Hỗ trợ hiển thị tốt trên thiết bị di động (Responsive)

---

## 8. Hướng phát triển

* Tích hợp thông báo real-time (Email / App Notification)
* Hiển thị bản đồ CLO–PLO cho sinh viên
* Mở rộng roadmap dạng cây trực quan

---

## 9. Kết luận

Student Web đóng vai trò là kênh tiếp cận chính thức giúp sinh viên dễ dàng tra cứu, hiểu rõ và theo dõi nội dung học phần. Phân hệ này góp phần nâng cao tính minh bạch và hiệu quả trong quản lý chương trình đào tạo của hệ thống SMD.

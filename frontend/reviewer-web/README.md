# Reviewer Web – Hệ thống Quản lý & Số hóa Giáo trình (SMD)

## 1. Giới thiệu

Reviewer Web là một phân hệ thuộc **Hệ thống Quản lý và Số hóa Giáo trình (Syllabus Management and Digitalization System – SMD)**. Phân hệ này được xây dựng nhằm hỗ trợ các cấp quản lý học thuật như **Trưởng Bộ môn (Head of Department – HoD)** và **Phòng Đào tạo (Academic Affairs – AA)** trong việc rà soát, so sánh, phê duyệt hoặc từ chối các phiên bản đề cương học phần (syllabus) theo đúng quy trình học thuật của nhà trường.

Hệ thống giúp tăng tính minh bạch, nhất quán và hiệu quả trong công tác quản lý đề cương, đồng thời hỗ trợ phát hiện thay đổi thông qua công cụ AI Change Detection.

---

## 2. Đối tượng sử dụng

* Trưởng Bộ môn (HoD)
* Phòng Đào tạo (Academic Affairs)
* Các giảng viên/nhân sự được phân quyền reviewer

---

## 3. Chức năng chính

### 3.1 Bảng điều khiển Reviewer (Dashboard)

* Hiển thị danh sách các syllabus đang chờ duyệt
* Truy cập nhanh vào trang chi tiết syllabus cần review

### 3.2 Review chi tiết Syllabus

* Xem đầy đủ thông tin syllabus: mã môn, tên môn, phiên bản, trạng thái, nội dung
* Phê duyệt syllabus (Approve)
* Từ chối syllabus kèm lý do bắt buộc (Reject with reason)
* Hộp thoại xác nhận khi thực hiện các thao tác quan trọng

### 3.3 So sánh các phiên bản Syllabus (Compare)

* So sánh song song phiên bản cũ và phiên bản mới
* Làm nổi bật các nội dung thay đổi (mô tả, CLO, đánh giá, tài liệu học tập)
* Hiển thị kết quả AI Change Detection để hỗ trợ reviewer ra quyết định nhanh

### 3.4 AI Change Detection (sẵn sàng tích hợp)

* Hiển thị các thay đổi được phát hiện bởi AI
* Có thể mở rộng tích hợp các mô hình NLP để so sánh ngữ nghĩa (Semantic Diff)

---

## 4. Công nghệ sử dụng

### Frontend

* HTML5
* CSS3 (Static CSS dùng chung)
* JavaScript thuần (Vanilla JS)

### Backend (tích hợp)

* Python FastAPI
* Jinja2 Template Engine

### Kiến trúc

* Mô hình Client – Server
* Phân quyền theo vai trò (RBAC)
* Tách biệt rõ giao diện, xử lý nghiệp vụ và dữ liệu

---

## 5. Cấu trúc thư mục

```
reviewer-web/
├── static/
│   ├── css/
│   │   └── reviewer.css
│   └── js/
│       └── reviewer.js
├── templates/
│   ├── dashboard.html
│   ├── review_detail.html
│   └── compare.html
└── routes.py
```

---

## 6. Tài nguyên Static

### CSS (`reviewer.css`)

* Định dạng giao diện chung
* Style bảng dữ liệu
* Style nút Approve / Reject
* Highlight nội dung thay đổi
* Giao diện AI Change Detection

### JavaScript (`reviewer.js`)

JavaScript được sử dụng ở mức tối thiểu, chỉ nhằm xác nhận các thao tác quan trọng:

```javascript
function confirmApprove() {
    return confirm("Bạn có chắc chắn muốn phê duyệt syllabus này không?");
}

function confirmReject() {
    return confirm("Bạn có chắc chắn muốn từ chối syllabus này không?");
}
```

---

## 7. Luồng nghiệp vụ (Workflow)

1. Giảng viên nộp syllabus mới hoặc cập nhật
2. Syllabus xuất hiện trong Dashboard của Reviewer
3. Reviewer mở trang chi tiết syllabus
4. Reviewer có thể:

   * Phê duyệt syllabus → chuyển sang cấp duyệt tiếp theo
   * Từ chối syllabus → trả về giảng viên kèm lý do
5. Reviewer có thể sử dụng chức năng so sánh phiên bản trước khi quyết định

---

## 8. Yêu cầu phi chức năng

* Giao diện đơn giản, dễ sử dụng
* JavaScript tối giản để giảm độ phức tạp
* Xử lý nghiệp vụ tập trung ở backend
* Dễ bảo trì và mở rộng trong tương lai

---

## 9. Hướng phát triển

* Phê duyệt không tải lại trang (AJAX)
* Highlight thay đổi nâng cao theo mức độ
* Tích hợp đầy đủ AI Microservice
* Thống kê và báo cáo học thuật

---

## 10. Kết luận

Reviewer Web cung cấp một giao diện rõ ràng, hiệu quả và đúng chuẩn học thuật cho công tác rà soát và phê duyệt syllabus. Phân hệ được xây dựng theo đúng nguyên tắc Công nghệ Phần mềm, đảm bảo tính mở rộng, dễ bảo trì và phù hợp với quy trình quản lý đào tạo của nhà trường.

---


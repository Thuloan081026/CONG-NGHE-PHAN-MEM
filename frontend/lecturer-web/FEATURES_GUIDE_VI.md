# Hướng Dẫn Sử Dụng Lecturer Web - SMD System

## 📋 Tổng Quan

Hệ thống SMD (Syllabus Management Dashboard) cung cấp đầy đủ các chức năng cho giảng viên quản lý đề cương môn học.

---

## 🔐 01. Đăng nhập / Đăng xuất

### Đăng nhập:
1. Truy cập trang **Login** tại `http://localhost:3000`
2. Nhập **email/tên đăng nhập** và **mật khẩu** của bạn
3. Nhấn **"Đăng nhập"**
4. Nếu thành công, bạn sẽ được chuyển đến **Dashboard**

### Đăng xuất:
- Nhấn vào **tên người dùng** ở góc trên bên phải
- Chọn **"Logout"**
- Bạn sẽ được chuyển về trang đăng nhập

---

## 📚 02. Tạo Mới Syllabus

### Bước 1: Truy cập trang Tạo Đề cương
- Từ Dashboard, nhấn **"Create New Syllabus"** (nút xanh)
- Hoặc vào menu: **My Syllabuses > Create New**

### Bước 2: Nhập thông tin cơ bản
- **Subject Code**: Mã môn (vd: CS201)
- **Subject Name**: Tên môn (vd: Data Structures)
- **Credits**: Số tín chỉ (vd: 3)
- **Semester**: Học kỳ
- **Description**: Mô tả ngắn gọn về môn học

### Bước 3: Định nghĩa CLO (Course Learning Outcomes)
- Nhấn **"+ Add CLO"** để thêm mục tiêu học tập
- Mỗi CLO nên cụ thể, đo lường được:
  - **CLO 1**: Hiểu được các cấu trúc dữ liệu cơ bản
  - **CLO 2**: Có khả năng thiết kế và triển khai thuật toán hiệu quả
  - ...

### Bước 4: Xác định PLO (Program Learning Outcomes)
- Các PLO là mục tiêu của chương trình đào tạo
- Thường được định nghĩa bởi trường/khoa
- Nhấn **"+ Add PLO"** để liên kết

### Bước 5: Ánh xạ CLO-PLO (CLO-PLO Mapping)
- Xác định CLO nào liên kết với PLO nào
- Ví dụ: CLO 1 hỗ trợ PLO 1, PLO 3

### Bước 6: Nội dung chương trình
- Danh sách các chương/bài học
- Cho mỗi chương, nhập:
  - **Chapter Name**: Tên chương
  - **Topics**: Các chủ đề chính
  - **Hours**: Số giờ giảng dạy
  - **CLOs Covered**: CLOs liên quan

### Bước 7: Phương pháp giảng dạy
- Chọn các phương pháp:
  - ☑ Lecture (Bài giảng)
  - ☑ Tutorial (Hướng dẫn)
  - ☑ Lab/Practical (Thực hành)
  - ☑ Project-based Learning
  - ...

### Bước 8: Phương pháp đánh giá
- **Attendance** (Chuyên cần): % trọng số
- **Assignment** (Bài tập): % trọng số
- **Midterm** (Giữa kỳ): % trọng số
- **Final Exam** (Cuối kỳ): % trọng số
- **Project** (Đồ án): % trọng số
- **Other**: % trọng số
- ⚠️ **Tổng phải = 100%**

### Bước 9: Thêm quan hệ môn học
- **Prerequisites** (Môn tiên quyết): Phải học trước
- **Corequisites** (Môn song hành): Học cùng thời gian
- **Equivalent Subjects** (Môn tương đương): Có cùng nội dung
- Ví dụ: CS101 (Tiên quyết) → CS201

### Bước 10: Tài liệu tham khảo
- **Textbooks**: Giáo trình chính
  - Tên sách
  - Tác giả
  - Năm xuất bản
  - ISBN (nếu có)
- **References**: Tài liệu tham khảo thêm
- **Learning Materials**: Slide, video, tài liệu hỗ trợ

### Bước 11: Auto-save (Tự động lưu)
- Hệ thống tự động lưu bản nháp **mỗi 2 phút**
- Bạn có thể đóng trình duyệt mà không mất dữ liệu
- Trạng thái: **Draft** (Bản nháp)

### Bước 12: Gửi để phê duyệt
- Khi hoàn thành, nhấn **"Submit for Review"**
- Trạng thái chuyển thành: **Submitted**

---

## ✏️ 03. Chỉnh sửa & Cập nhật Phiên bản Syllabus

### Bước 1: Vào quản lý phiên bản
- Từ Dashboard → **"Version History"** (nút xanh)
- Hoặc: Menu → **Syllabus Management > Version History**

### Bước 2: Chọn đề cương
- Từ dropdown **"Chọn Đề cương"**, chọn môn học bạn muốn chỉnh sửa

### Bước 3: Xem lịch sử phiên bản
- Danh sách **Phiên bản** hiển thị ở bên trái
- Mỗi phiên bản có:
  - Số version (v1, v2, v3...)
  - Trạng thái (Draft, Submitted, Approved...)
  - Ngày tạo
  - Tóm tắt thay đổi

### Bước 4: So sánh phiên bản (AI Semantic Diff)
1. Chọn **"Phiên bản cũ"** (Phiên bản cũ)
2. Chọn **"Phiên bản mới"** (Phiên bản mới)
3. Hệ thống sẽ tự động:
   - **Detect changes** (Phát hiện thay đổi)
   - Hiển thị **Green** (Phần thêm)
   - Hiển thị **Red** (Phần xóa)
   - So sánh từng trường: CLO, PLO, nội dung, đánh giá...

### Bước 5: Chỉnh sửa phiên bản
- Nhấn **"Edit"** trên phiên bản cũ
- Hệ thống sẽ tải dữ liệu cũ vào form
- Bạn chỉnh sửa các trường cần thiết
- Khi lưu, sẽ tạo **phiên bản mới**
- Tự động lưu bản nháp

### Bước 6: Gửi lên HoD
1. Chọn phiên bản cuối cùng bạn muốn gửi
2. Nhấn **"Gửi lên HoD để phê duyệt"** (nút xanh)
3. Trạng thái: **Submitted** → Chờ HoD phê duyệt
4. Bạn sẽ nhận thông báo khi HoD xem xét

### Bước 7: Khôi phục phiên bản
- Nếu cần quay lại phiên bản cũ:
  1. Chọn phiên bản muốn khôi phục
  2. Nhấn **"Khôi phục phiên bản"**
  3. Dữ liệu sẽ được tạo thành phiên bản mới (v_restored)

---

## 💬 04. Tham gia Collaborative Review

### Bước 1: Xem yêu cầu xem xét
- Vào **Dashboard** → **"Collaborative Review"**
- Hoặc: Menu → **Collaboration > Collaborative Review**
- Tab **"Yêu cầu xem xét cho tôi"** hiển thị các đề cương từ đồng nghiệp

### Bước 2: Xem xét đề cương
1. Tìm đề cương cần review
2. Nhấn **"Xem xét"** (nút xanh)
3. Modal hiển thị:
   - Thông tin cơ bản
   - CLO, PLO, nội dung
   - Phương pháp giảng dạy, đánh giá

### Bước 3: Đưa ra nhận xét
- Viết nhận xét chi tiết trong textbox
- Chọn loại nhận xét:
  - ☐ **Góp ý** (Suggestion): Cải thiện không bắt buộc
  - ☐ **Vấn đề cần sửa** (Concern): Cần chỉnh sửa
  - ☑ **Phê duyệt** (Approved): Đồng ý
- Nhấn **"Gửi nhận xét"**

### Bước 4: Xem phản hồi từ đồng nghiệp
- Tab **"Đề cương của tôi đang review"**
- Hiển thị:
  - Người đang xem xét
  - Bình luận/nhận xét của họ
  - Phản hồi từ HoD
- Bạn có thể **trả lời** bình luận bằng cách:
  1. Viết trong ô **"Trả lời những bình luận..."**
  2. Nhấn **"Trả lời"**

### Bước 5: Chỉnh sửa theo yêu cầu
1. Nếu có góp ý hoặc vấn đề:
   - Vào **Version History**
   - Chỉnh sửa đề cương
   - Tạo phiên bản mới
   - Tự động thông báo cho reviewers

---

## 📖 05. Quản lý Syllabus Cá nhân

### Bước 1: Xem danh sách đề cương
- **Dashboard** → **"View All Syllabuses"**
- Hoặc: Menu → **My Syllabuses > View All**

### Bước 2: Lọc & Tìm kiếm
- **Tìm kiếm**: Nhập mã hoặc tên môn học
- **Lọc theo Trạng thái**:
  - All Status (Tất cả)
  - Draft (Bản nháp)
  - Submitted (Đã gửi)
  - Under Review (Đang review)
  - Approved (Phê duyệt)
  - Published (Công bố)
- **Lọc theo Học kỳ**: 1, 2, 3...

### Bước 3: So sánh phiên bản qua AI
1. Chọn một đề cương
2. Vào **"Version History"**
3. Hệ thống sẽ:
   - Liệt kê tất cả phiên bản
   - Hiển thị những thay đổi **từng mục**:
     - Subject Code
     - CLOs
     - PLOs
     - Content
     - Assessment Methods
     - Textbooks
   - Sử dụng **Semantic Diff**: so sánh ý nghĩa, không chỉ từng ký tự

### Bước 4: Thao tác với từng Syllabus
Mỗi hàng trong bảng có các nút:
- **👁 View** (Xem): Xem chi tiết
- **✏️ Edit** (Chỉnh sửa): Chỉnh sửa phiên bản
- **🔄 History** (Lịch sử): Xem tất cả phiên bản
- **🗑 Delete** (Xóa): Xóa (chỉ Draft)

### Bước 5: Export & Share
- **Download PDF**: Xuất bản dưới dạng PDF
- **Share Link**: Chia sẻ link review với đồng nghiệp

---

## 🔔 06. Nhận Thông Báo

### Bước 1: Truy cập trang Thông báo
- **Dashboard** → **"View Notifications"** (nút cam)
- Hoặc: Menu → **Notifications**
- Hoặc: Biểu tượng 🔔 góc trên (hiển thị số thông báo chưa đọc)

### Bước 2: Các loại thông báo
1. **📤 Đơn gửi** (Submission):
   - Khi bạn gửi đề cương lên
   - Xác nhận HoD nhận được
   
2. **✏️ Review**:
   - Có người request xem xét đề cương của bạn
   - Có feedback từ đồng nghiệp
   - Có bình luận mới

3. **✅ Phê duyệt**:
   - HoD phê duyệt đề cương
   - Đề cương được công bố

4. **ℹ️ Hệ thống**:
   - Thông báo từ admin
   - Cập nhật chính sách

### Bước 3: Quản lý thông báo
- **Chưa đọc** (xanh): Các thông báo mới
- **Đã đọc** (xám): Các thông báo cũ
- **Cần hành động** (đỏ): Cần bạn làm gì đó

Các bộ lọc:
- 🔔 **Chưa đọc**: Chỉ hiển thị thông báo mới
- 📤 **Đơn gửi**: Liên quan đến submission
- ✏️ **Review**: Liên quan đến review
- ✅ **Phê duyệt**: Liên quan đến approval

### Bước 4: Hành động với thông báo
- Nhấn vào thông báo để xem chi tiết
- Nếu có **"Xem chi tiết"**, nhấn để xem đề cương liên quan
- **Đánh dấu tất cả đã đọc**: Xóa dấu chưa đọc

---

## 📊 Dashboard - Tổng Quan

### Các Card Thống Kê:
1. **Đề tài đề xuất**: Số đề cương chờ duyệt
2. **Lịch Review sắp tới**: Số lần review trong tuần
3. **Tin nhắn mới**: Số feedback từ nhóm
4. **Đề tài hoàn thành**: Số đề cương đã phê duyệt
5. **Bản nháp**: Số đề cương đang chỉnh sửa

### Recent Syllabuses:
- Danh sách 5 đề cương mới nhất
- Hiển thị trạng thái, ngày cập nhật
- Nút: **View** (Xem), **Edit** (Chỉnh sửa)

### Quick Actions:
- Truy cập nhanh đến các chức năng chính
- Tạo đề cương mới
- Xem danh sách
- Quản lý phiên bản
- Tham gia collaborative review

---

## ⚙️ Lưu Ý & Mẹo

### 💾 Auto-save (Tự động lưu)
- ✅ Khi tạo/chỉnh sửa, hệ thống tự động lưu **mỗi 2 phút**
- ✅ Bạn có thể tắt tab mà không mất dữ liệu
- ⚠️ Dữ liệu được lưu dưới **trạng thái Draft** (Bản nháp)

### 📝 Cách viết CLO hiệu quả
- Sử dụng **Bloom's Taxonomy**: Remember → Understand → Apply → Analyze → Evaluate → Create
- **Cụ thể**: "Students will be able to..."
- **Đo lường được**: "Design, implement, analyze..." (không dùng "know, understand")
- Ví dụ tốt: "Design and implement a binary search tree with O(log n) complexity"

### 🔍 Collaborative Review Best Practices
- ✅ Xem xét kỹ trước khi phê duyệt
- ✅ Cho nhận xét cụ thể, không chung chung
- ✅ Trả lời comment của reviewers trong 2-3 ngày
- ⚠️ Không thể thay đổi sau khi HoD phê duyệt (phải tạo phiên bản mới)

### 🔐 Bảo mật
- ✅ Luôn đảm bảo bạn đã **logout** trên máy công cộng
- ✅ Không chia sẻ token/access_token
- ✅ Mật khẩu tối thiểu 8 ký tự, có chữ hoa, số, ký tự đặc biệt

---

## ❓ FAQ

**Q: Tôi quên mật khẩu, phải làm sao?**
A: Nhấn "Forgot Password" trên trang login. Hệ thống sẽ gửi link reset về email.

**Q: Phiên bản đã gửi có thể chỉnh sửa không?**
A: Có, nhưng chỉ tạo thành phiên bản mới. Phiên bản cũ vẫn giữ nguyên.

**Q: Làm sao để biết HoD đã review?**
A: Kiểm tra **Notifications** hoặc **Collaborative Review** tab "Đề cương của tôi".

**Q: Có thể xóa đề cương không?**
A: Chỉ có thể xóa đề cương ở **trạng thái Draft**. Sau khi submit không thể xóa.

**Q: Làm cách nào để lấy lại đề cương cũ?**
A: Vào **Version History**, chọn phiên bản cũ, nhấn **"Khôi phục phiên bản"**.

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra email đăng nhập có chính xác không
2. Xóa cache trình duyệt (Ctrl+Shift+Delete)
3. Thử đăng nhập lại
4. Liên hệ **Admin** hoặc **IT Support**

---

**Cập nhật lần cuối**: 06/01/2026
**Phiên bản**: 2.0.0

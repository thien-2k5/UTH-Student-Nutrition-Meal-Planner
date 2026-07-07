# Bảng Theo Dõi Công Việc (Tasks Checklist)
> **UTH Student Nutrition Meal Planner**

Tài liệu này lưu trữ danh mục công việc cần hoàn thành trong dự án xây dựng ứng dụng web dinh dưỡng cho sinh viên UTH.

---

## 📅 Tiến Độ Thực Hiện

- [x] **1. Thiết Lập Dự Án & Cấu Hình**
  - [x] Tạo tệp chứa các thư viện Python: [requirements.txt](file:///Users/thien/Documents/learn/TDTKDMST/requirements.txt)
  - [x] Thiết lập cấu hình ứng dụng: [config.py](file:///Users/thien/Documents/learn/TDTKDMST/config.py)
  - [x] Tạo tệp cấu hình biến môi trường mẫu: [.env.example](file:///Users/thien/Documents/learn/TDTKDMST/.env.example)
  - [x] Thiết lập bỏ qua tệp tin rác của Git: [.gitignore](file:///Users/thien/Documents/learn/TDTKDMST/.gitignore)
  - [x] Tạo tệp bản quyền phần mềm: [LICENSE](file:///Users/thien/Documents/learn/TDTKDMST/LICENSE)

- [x] **2. Cấu Trúc Cơ Sở Dữ Liệu & Dữ Liệu Mẫu**
  - [x] Định nghĩa SQLAlchemy Model cho món ăn: [models/food.py](file:///Users/thien/Documents/learn/TDTKDMST/models/food.py)
  - [x] Viết script nạp dữ liệu mẫu SQLite: [database/seed.py](file:///Users/thien/Documents/learn/TDTKDMST/database/seed.py)
  - [x] Nạp thành công hơn 100 món ăn Việt Nam bình dân quen thuộc cho sinh viên.

- [x] **3. Dịch Vụ Tính Toán & Xử Lý Logic (Service Layer)**
  - [x] Triển khai logic tính toán BMI, BMR, TDEE, lượng nước: [services/calculator.py](file:///Users/thien/Documents/learn/TDTKDMST/services/calculator.py)
  - [x] Phát triển thuật toán đề xuất thực đơn ngẫu nhiên có ràng buộc chi phí và calo mục tiêu: [services/recommender.py](file:///Users/thien/Documents/learn/TDTKDMST/services/recommender.py)
  - [x] Xây dựng bộ phân tích biểu thức chính quy (Regex) và gọi API Chatbot: [services/chatbot.py](file:///Users/thien/Documents/learn/TDTKDMST/services/chatbot.py)

- [x] **4. Thiết Kế Điều Hướng & Viết REST API (Controller Layer)**
  - [x] Viết tệp khởi chạy ứng dụng Flask: [app.py](file:///Users/thien/Documents/learn/TDTKDMST/app.py)
  - [x] Viết các routes điều hướng trang và endpoints xử lý API: [routes/main.py](file:///Users/thien/Documents/learn/TDTKDMST/routes/main.py)

- [x] **5. Xây Dựng Giao Diện Người Dùng (Views / HTML Templates)**
  - [x] Thiết lập giao diện layout chung (Navbar, Footer, Chatbot widget): [templates/components/base.html](file:///Users/thien/Documents/learn/TDTKDMST/templates/components/base.html)
  - [x] Thiết kế trang chủ Hero đẹp mắt: [templates/index.html](file:///Users/thien/Documents/learn/TDTKDMST/templates/index.html)
  - [x] Thiết kế trang tính BMI tương tác: [templates/bmi.html](file:///Users/thien/Documents/learn/TDTKDMST/templates/bmi.html)
  - [x] Thiết kế trang đề xuất thực đơn, đồ thị phân tích: [templates/recommend.html](file:///Users/thien/Documents/learn/TDTKDMST/templates/recommend.html)
  - [x] Thiết kế trang chat chuyên dụng: [templates/chat.html](file:///Users/thien/Documents/learn/TDTKDMST/templates/chat.html)
  - [x] Thiết kế trang cẩm nang kiến thức: [templates/knowledge.html](file:///Users/thien/Documents/learn/TDTKDMST/templates/knowledge.html)
  - [x] Thiết kế trang giới thiệu và liên hệ: [templates/about.html](file:///Users/thien/Documents/learn/TDTKDMST/templates/about.html)
  - [x] Thiết kế các trang báo lỗi tùy biến: 404 và 500.

- [x] **6. Phát Triển Tệp Tĩnh CSS & JavaScript (Assets)**
  - [x] Viết file CSS phong cách Modern Food Glassmorphism & Dark Mode: [static/css/main.css](file:///Users/thien/Documents/learn/TDTKDMST/static/css/main.css)
  - [x] Viết file JS điều khiển BMI, Recommend, Chart.js, PDF và CSV: [static/js/main.js](file:///Users/thien/Documents/learn/TDTKDMST/static/js/main.js)
  - [x] Viết file JS điều phối tin nhắn chatbot và bong bóng nổi: [static/js/chat.js](file:///Users/thien/Documents/learn/TDTKDMST/static/js/chat.js)

- [x] **7. Kiểm Thử & Biên Soạn Tài Liệu**
  - [x] Viết bộ kiểm thử tự động kiểm nghiệm các API và hàm tính toán: [tests/test_app.py](file:///Users/thien/Documents/learn/TDTKDMST/tests/test_app.py)
  - [x] Hoàn thiện các tài liệu đặc tả dự án (`README.md`, `architecture.md`, `roadmap.md`, `features.md`, `api.md`, `database.md`, `deployment.md`, `CHANGELOG.md`).

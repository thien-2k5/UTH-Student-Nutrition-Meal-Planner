# Nhật Ký Thay Đổi Phiên Bản (Changelog)
> **UTH Student Nutrition Meal Planner**

Tất cả các thay đổi chính thức của dự án sẽ được ghi nhận tại tệp tin này.

---

## [1.0.0] - 2026-07-07

### 🚀 Tính năng nổi bật
- **BMI & TDEE Calculator**: Công thức Mifflin-St Jeor chuẩn hóa, có biểu đồ thang đo BMI và tính toán nước uống.
- **Smart Meal Recommender**: Thuật toán chọn bữa ăn ngẫu nhiên thỏa mãn ràng buộc ngân sách ăn hàng ngày (từ 40k, 50k, 70k, 100k, 150k) và tối ưu hóa lượng Calo/Protein theo BMI.
- **Seeded Foods DB**: Cơ sở dữ liệu SQLite được nạp sẵn 115 món ăn Việt Nam bình dân quen thuộc cho sinh viên.
- **Interactive Charts Dashboard**: Vẽ đồ thị Doughnut hiển thị cơ cấu Macro dinh dưỡng, đồ thị Bar đối chiếu năng lượng và chi tiêu bằng Chart.js.
- **Contextual Chatbot**: Hệ thống chatbot nhận diện thông số tự động bằng biểu thức chính quy (Regex), có cơ chế lưu trữ session và tích hợp sẵn Gemini AI / OpenAI API.
- **Export Utilities**: In ấn thực đơn hoặc xuất PDF thông qua CSS print media sạch đẹp, hỗ trợ tải về bảng dinh dưỡng file CSV.
- **Modern Food Glassmorphism & Dark Mode**: Thiết kế kính mờ hiện đại, hỗ trợ chế độ ban đêm bảo vệ mắt sinh viên, tương thích hoàn toàn trên Mobile và Desktop.

### 📁 Các tệp mã nguồn khởi tạo
- **Cấu hình & Điểm bắt đầu**: `requirements.txt`, `config.py`, `app.py`, `.env.example`, `.gitignore`, `LICENSE`
- **Database & Model**: `database/seed.py`, `models/food.py`, `database/db.py`
- **Tầng xử lý logic**: `services/calculator.py`, `services/recommender.py`, `services/chatbot.py`
- **Tầng kiểm soát & hiển thị**: `routes/main.py`, `templates/`
- **Giao diện tĩnh**: `static/css/main.css`, `static/js/main.js`, `static/js/chat.js`
- **Tài liệu**: `README.md`, `architecture.md`, `roadmap.md`, `features.md`, `api.md`, `database.md`, `deployment.md`, `tasks.md`, `CHANGELOG.md`
- **Kiểm thử tự động**: `tests/test_app.py`

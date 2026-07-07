# UTH Student Nutrition Meal Planner
> **Hệ thống xây dựng thực đơn dinh dưỡng dành cho sinh viên UTH**

Một ứng dụng web được xây dựng bằng Python (Flask), SQLite và JavaScript (Bootstrap 5, Chart.js) giúp sinh viên trường **Đại học Giao thông vận tải Thành phố Hồ Chí Minh (UTH)** tối ưu hóa chế độ dinh dưỡng hàng ngày phù hợp với túi tiền sinh viên.

---

## 🌟 Tính Năng Nổi Bật

- **Tính toán BMI & TDEE khoa học**: Ước tính chỉ số khối cơ thể (BMI) và tổng năng lượng tiêu thụ hàng ngày (TDEE) bằng phương trình Mifflin-St Jeor.
- **Đề xuất thực đơn theo ngân sách ngày**: Thuật toán tự động tìm tổ hợp 4 bữa ăn (Sáng, Trưa, Tối, Phụ/Nước) phù hợp với ngân sách chỉ từ 40.000đ/ngày, đảm bảo cân đối đạm, tinh bột, chất béo, xơ và vitamin.
- **AI Chatbot hỗ trợ 24/7**: Chatbot thông minh tự động nhận diện dữ liệu thể chất từ cuộc đối thoại tự nhiên, đồng thời tích hợp Gemini AI/OpenAI API khi được cung cấp Key.
- **Dashboard Phân Tích Dinh Dưỡng**: Biểu đồ Chart.js trực quan hóa tỷ lệ các chất đa lượng (Macro) và biểu đồ cột so sánh Calo/Ngân sách.
- **Tiện ích xuất dữ liệu**: Hỗ trợ in thực đơn, xuất file PDF, hoặc tải về file CSV.
- **Giao diện Modern Food UI**: Thiết kế glassmorphism hiện đại, hỗ trợ Dark Mode hoàn chỉnh và tương thích hoàn hảo trên các thiết bị di động.

---

## 🛠️ Công Nghệ Sử Dụng

- **Backend**: Python 3.12+, Flask Framework
- **Database**: SQLite, Flask-SQLAlchemy ORM
- **Frontend**: HTML5, CSS3 (Vanilla Glassmorphism), Bootstrap 5, Jinja2 template
- **Charts**: Chart.js
- **Testing**: Pytest

---

## 📂 Cấu Trúc Thư Mục Dự Án

```text
project/
├── app.py                  # Điểm khởi chạy ứng dụng Flask
├── config.py               # Tệp cấu hình ứng dụng
├── requirements.txt        # Các thư viện Python cần thiết
├── README.md               # Hướng dẫn chung
├── LICENSE                 # Giấy phép MIT
├── .gitignore              # Chỉ định các tệp Git bỏ qua
├── .env.example            # Bản mẫu cấu hình môi trường
├── architecture.md         # Tài liệu kiến trúc hệ thống
├── roadmap.md              # Lộ trình phát triển dự án
├── features.md             # Tài liệu chi tiết các tính năng
├── api.md                  # Tài liệu đặc tả REST API
├── database.md             # Cấu trúc và lược đồ cơ sở dữ liệu
├── deployment.md           # Hướng dẫn triển khai lên Cloud
├── tasks.md                # Danh sách công việc triển khai
├── CHANGELOG.md            # Nhật ký thay đổi phiên bản
├── database/
│   ├── food.db             # Cơ sở dữ liệu SQLite chứa thực đơn
│   └── seed.py             # Script nạp sẵn 115 món ăn Việt Nam
├── models/
│   └── food.py             # Định nghĩa cấu trúc bảng Food
├── routes/
│   └── main.py             # Xử lý các đường dẫn Web & API endpoints
├── services/
│   ├── calculator.py       # Logic tính BMI, BMR, TDEE
│   ├── recommender.py      # Thuật toán tìm kiếm bữa ăn
│   └── chatbot.py          # Xử lý nhận dạng tham số & AI chatbot
├── static/
│   ├── css/
│   │   └── main.css        # File CSS chính với Glassmorphism & Dark Mode
│   └── js/
│   │   ├── main.js         # Logic xử lý giao diện & đồ thị Chart.js
│   │   └── chat.js         # Logic xử lý tin nhắn chatbot
├── templates/
│   ├── components/
│   │   ├── base.html       # Giao diện khung dùng chung (Navbar, Footer, Chatbot trigger)
│   │   ├── 404.html        # Trang báo lỗi 404
│   │   └── 500.html        # Trang báo lỗi 500
│   ├── index.html          # Trang chủ / Landing page
│   ├── bmi.html            # Trang tính chỉ số BMI & TDEE
│   ├── recommend.html      # Trang gợi ý thực đơn & biểu đồ
│   ├── chat.html           # Trang trò chuyện chuyên dụng
│   ├── knowledge.html      # Trang cẩm nang kiến thức dinh dưỡng
│   └── about.html          # Trang giới thiệu dự án
└── tests/
    └── test_app.py         # Kiểm thử tự động (Unit test)
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Thử

### Bước 1: Sao chép mã nguồn (Clone repository) hoặc di chuyển vào thư mục dự án
```bash
cd /Users/thien/Documents/learn/UTH-Student-Nutrition-Meal-Planner
```

### Bước 2: Tạo môi trường ảo và cài đặt thư viện
```bash
# Tạo môi trường ảo (Khuyên dùng)
python3 -m venv venv
source venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### Bước 3: Cấu hình môi trường
Sao chép tệp `.env.example` thành `.env` và thiết lập khóa (nếu có):
```bash
cp .env.example .env
```

### Bước 4: Tạo và nạp dữ liệu mẫu món ăn (Database Seeding)
Chạy script để khởi tạo cơ sở dữ liệu `food.db` và nạp hơn 100 món ăn Việt Nam:
```bash
python3 database/seed.py
```

### Bước 5: Chạy ứng dụng web
Khởi chạy Flask server cục bộ:
```bash
python3 app.py
```
Ứng dụng sẽ chạy tại địa chỉ: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Chạy Kiểm Thử Tự Động (Unit Tests)
Chạy pytest để xác minh tính chính xác của các thuật toán tính toán và đề xuất:
```bash
pytest
```

# Đặc Tả Tính Năng Chi Tiết (Features Specifications)
> **UTH Student Nutrition Meal Planner**

Tài liệu này liệt kê toàn bộ các tính năng đã được triển khai trong ứng dụng và cách thức hoạt động của chúng.

---

## 🎯 Danh Sách Tính Năng

### 1. Tính toán BMI & TDEE
- **Nhập liệu**: Người dùng nhập giới tính, tuổi, chiều cao, cân nặng, mức vận động hàng tuần.
- **Tính toán**:
  - Hệ thống tính toán BMI, BMR, TDEE, lượng nước tối thiểu cần uống mỗi ngày.
  - Phân loại trạng thái thể lực: Gầy, Bình thường, Thừa cân, Béo phì.
- **Hiển thị**: Thanh thang đo chỉ số BMI hiển thị phân vùng trạng thái bằng màu sắc trực quan (Xanh dương, xanh lá, vàng, đỏ).

### 2. Lập thực đơn thông minh theo ngân sách
- **Thiết lập mục tiêu**: Lựa chọn chế độ duy trì cân nặng, tăng cân hoặc giảm cân.
- **Ngân sách linh hoạt**: Lựa chọn hạn mức chi tiêu hàng ngày (40.000đ, 50.000đ, 70.000đ, 100.000đ, 150.000đ).
- **Phân bổ bữa ăn**: Đề xuất thực đơn gồm 4 bữa rõ ràng (Sáng, Trưa, Tối, Phụ/Nước) với giá và calo cụ thể của từng món.
- **Tối ưu hóa đa lượng (Macros)**: Đảm bảo lượng Protein cao và lượng Calo tiệm cận mục tiêu nhất trong tầm giá.
- **Chuyển đổi nhanh**: Nút "Đổi thực đơn khác" giúp làm mới thực đơn ngẫu nhiên ngay lập tức nếu sinh viên không thích thực đơn hiện tại.

### 3. Đồ thị phân tích Dinh dưỡng & Chi phí
- **Tỷ lệ đa lượng**: Biểu đồ tròn Doughnut biểu diễn phần trăm năng lượng đến từ Protein, Carbs, Fats.
- **Đối chiếu calo**: Biểu đồ cột Bar đối sánh năng lượng thực đơn đề xuất với năng lượng mục tiêu.
- **Đối chiếu ngân sách**: Biểu đồ cột Bar đối sánh chi phí thực tế với ngân sách người dùng đề ra.

### 4. AI Chatbot thông minh
- **Nhận diện tự động**: Sử dụng Regular Expressions (Regex) để tự động trích xuất các thông số thể lực trong câu nói tự nhiên của người dùng (ví dụ: "mình cao 170 nặng 60kg cần ăn 50k").
- **Ghi nhớ ngữ cảnh**: Sử dụng cơ chế lưu session trên Flask để tích lũy dần các thông tin thiếu qua đối thoại và trả về kết quả phân tích đầy đủ khi nhận đủ thông tin.
- **Tích hợp API kép**: Tự động kết nối với Gemini AI (mặc định) hoặc OpenAI GPT khi phát hiện API Key tương ứng trong biến môi trường.
- **Hỏi đáp kiến thức**: Trả lời nhanh các thắc mắc về vai trò của Protein, Carbs, Chất béo, nước uống và các lời khuyên cho đời sống sinh viên.

### 5. Tra cứu dữ liệu món ăn Việt Nam
- **Bộ lọc đa dạng**: Hỗ trợ tìm kiếm theo tên món ăn, danh mục bữa ăn (Sáng, Trưa, Tối, Ăn vặt, Nước uống).
- **Bộ lọc giới hạn**: Tìm kiếm các món ăn có mức giá hoặc calo nhỏ hơn hạn mức tự định nghĩa.
- **Live Search**: Kết quả tìm kiếm tự động cập nhật ngay khi người dùng gõ phím (có cơ chế Debounce 400ms tránh nghẽn mạng).

### 6. Tiện ích xuất dữ liệu
- **Xuất PDF / In ấn**: Định dạng in chuyên nghiệp (CSS @media print tự động ẩn thanh điều hướng, chatbot, các nút bấm để tạo ra bản in thực đơn sạch đẹp).
- **Tải tệp CSV**: Chuyển đổi thực đơn đề xuất thành tệp dữ liệu CSV chuẩn UTF-8 (có chèn BOM) tương thích tốt với Microsoft Excel.

### 7. Tối ưu hóa UI/UX
- **Đồ họa Glassmorphic**: Nền mờ đục ảo diệu, bo góc mềm mại, đổ bóng sâu tạo chiều sâu thị giác.
- **Dark Mode**: Chuyển đổi toàn diện giao diện Sáng / Tối giúp bảo vệ mắt sinh viên khi lướt web ban đêm, tự động lưu preference vào LocalStorage.
- **Hiệu ứng tải trang**: Loading overlay ngăn chặn thao tác lỗi khi hệ thống đang xử lý API.
- **Toast Notifications**: Hộp thông báo nhanh gọn ở góc màn hình không cản trở trải nghiệm người dùng.

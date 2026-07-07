# Đặc Tả REST API (API Specifications)
> **UTH Student Nutrition Meal Planner**

Tài liệu này đặc tả chi tiết các cổng giao tiếp API (endpoints) được thiết lập trong ứng dụng để phục vụ giao tiếp bất đồng bộ giữa Frontend và Backend.

---

## 🧭 Danh Sách Endpoints

### 1. Tính toán BMI, BMR và TDEE
- **Đường dẫn**: `/api/bmi`
- **Phương thức**: `POST`
- **Kiểu dữ liệu**: `application/json`

**Yêu cầu (Request Body):**
```json
{
  "weight": 60,
  "height": 170,
  "age": 20,
  "gender": "nam",
  "activity": "moderately_active"
}
```
*Ghi chú:* `activity` chấp nhận các giá trị: `sedentary`, `lightly_active`, `moderately_active`, `very_active`, `extra_active`.

**Phản hồi thành công (Response 200 OK):**
```json
{
  "success": true,
  "bmi": 20.76,
  "classification": "Bình thường",
  "bmr": 1505.0,
  "tdee": 2332.75
}
```

---

### 2. Gợi ý thực đơn hàng ngày
- **Đường dẫn**: `/api/recommend`
- **Phương thức**: `POST`
- **Kiểu dữ liệu**: `application/json`

**Yêu cầu (Request Body):**
```json
{
  "weight": 60,
  "height": 170,
  "age": 20,
  "gender": "nam",
  "activity": "moderately_active",
  "budget": 70000,
  "goal": "lose"
}
```
*Ghi chú:* `goal` chấp nhận các giá trị: `maintain` (giữ cân), `lose` (giảm cân), `gain` (tăng cân).

**Phản hồi thành công (Response 200 OK):**
```json
{
  "success": true,
  "bmi": 20.76,
  "classification": "Bình thường",
  "tdee": 2332.75,
  "target_calories": 1932.75,
  "menu": [
    { "id": 1, "name": "Bánh mì pate chả lụa", "price": 18000.0, "calories": 380.0, "protein": 14.2, "carb": 42.0, "fat": 12.5, "fiber": 2.0, "vitamin": "B1, B3, B6", "category": "Sáng" },
    { "id": 35, "name": "Cơm đậu hũ dồn thịt sốt cà", "price": 22000.0, "calories": 430.0, "protein": 18.5, "carb": 64.0, "fat": 12.0, "fiber": 3.2, "vitamin": "Canxi, Sắt, C, E", "category": "Trưa/Tối" },
    { "id": 40, "name": "Cơm trứng đúc thịt hành lá + canh", "price": 20000.0, "calories": 410.0, "protein": 16.5, "carb": 63.0, "fat": 11.5, "fiber": 1.5, "vitamin": "A, B12, D", "category": "Trưa/Tối" },
    { "id": 75, "name": "Sữa đậu nành UTH tự nấu", "price": 6000.0, "calories": 110.0, "protein": 6.5, "carb": 12.0, "fat": 4.0, "fiber": 1.5, "vitamin": "B1, B2, E, Phytoestrogen", "category": "Nước uống" }
  ],
  "breakfast": { "id": 1, "name": "Bánh mì pate chả lụa", ... },
  "lunch": { "id": 35, "name": "Cơm đậu hũ dồn thịt sốt cà", ... },
  "dinner": { "id": 40, "name": "Cơm trứng đúc thịt hành lá + canh", ... },
  "snack": { "id": 75, "name": "Sữa đậu nành UTH tự nấu", ... },
  "metrics": {
    "total_cost": 66000.0,
    "total_calories": 1330.0,
    "total_protein": 55.7,
    "total_fat": 40.0,
    "total_carb": 181.0,
    "total_fiber": 8.2
  }
}
```

---

### 3. Tương tác Chatbot
- **Đường dẫn**: `/api/chat`
- **Phương thức**: `POST`
- **Kiểu dữ liệu**: `application/json`

**Yêu cầu (Request Body):**
```json
{
  "message": "Mình cao 170cm, nặng 60kg, 20 tuổi, nam, tiền ăn 70k"
}
```

**Phản hồi thành công (Response 200 OK):**
```json
{
  "success": true,
  "reply": "### 📊 Kết Quả Phân Tích Dinh Dưỡng\n- **BMI của bạn**: 20.76 (Thể trạng: **Bình thường**)\n...",
  "state": {
    "height": 170,
    "weight": 60,
    "age": 20,
    "gender": "nam",
    "budget": 70000
  }
}
```

---

### 4. Tra cứu danh sách món ăn
- **Đường dẫn**: `/api/foods`
- **Phương thức**: `GET`
- **Tham số truy vấn (Query parameters)**:
  - `q` (Chuỗi tìm kiếm tên món ăn, không bắt buộc)
  - `category` (Lọc theo danh mục: `Sáng`, `Trưa/Tối`, `Ăn vặt`, `Nước uống`, không bắt buộc)
  - `max_price` (Giá tiền tối đa, không bắt buộc)
  - `max_calories` (Calo tối đa, không bắt buộc)

**Phản hồi thành công (Response 200 OK):**
```json
{
  "success": true,
  "count": 2,
  "foods": [
    { "id": 1, "name": "Bánh mì ốp la (1 trứng)", "price": 15000.0, "calories": 295.0, "protein": 11.5, "carb": 38.0, "fat": 9.8, "fiber": 1.8, "vitamin": "A, B12, D", "category": "Sáng" },
    { "id": 2, "name": "Bánh mì ốp la (2 trứng)", "price": 20000.0, "calories": 365.0, "protein": 17.5, "carb": 38.2, "fat": 15.0, "fiber": 1.8, "vitamin": "A, B12, D, E", "category": "Sáng" }
  ]
}
```

# Tài Liệu Cơ Sở Dữ Liệu (Database Schema)
> **UTH Student Nutrition Meal Planner**

Hệ thống sử dụng cơ sở dữ liệu **SQLite** gọn nhẹ, lưu trữ cục bộ dưới dạng tệp tin đơn tại đường dẫn `database/food.db`.

---

## 📊 Lược Đồ Bảng (Table Schema)

Hệ thống chỉ sử dụng một bảng chính mang tên `foods` dùng để lưu trữ danh sách các món ăn Việt Nam được nạp sẵn.

### Bảng: `foods`

| Tên Cột (Column) | Kiểu Dữ Liệu (Type) | Ràng Buộc (Constraints) | Mô Tả (Description) |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Khóa chính tự động tăng |
| `name` | TEXT / VARCHAR(150) | NOT NULL | Tên món ăn tiếng Việt |
| `price` | REAL / FLOAT | NOT NULL | Giá tiền tính bằng VND (ví dụ: 15000.0) |
| `protein` | REAL / FLOAT | NOT NULL | Lượng chất đạm tính bằng Grams |
| `fat` | REAL / FLOAT | NOT NULL | Lượng chất béo tính bằng Grams |
| `carb` | REAL / FLOAT | NOT NULL | Lượng chất tinh bột tính bằng Grams |
| `fiber` | REAL / FLOAT | NOT NULL | Lượng chất xơ tính bằng Grams |
| `vitamin` | TEXT / VARCHAR(250) | NOT NULL | Danh sách các Vitamin/Khoáng chất (ngăn cách bằng dấu phẩy) |
| `calories` | REAL / FLOAT | NOT NULL | Chỉ số năng lượng tính bằng kcal |
| `category` | TEXT / VARCHAR(50) | NOT NULL | Danh mục bữa ăn (`Sáng`, `Trưa/Tối`, `Ăn vặt`, `Nước uống`) |

---

## 🛠️ Câu Lệnh Khởi Tạo SQL (DDL Statement)

```sql
CREATE TABLE foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    protein REAL NOT NULL,
    fat REAL NOT NULL,
    carb REAL NOT NULL,
    fiber REAL NOT NULL,
    vitamin TEXT NOT NULL,
    calories REAL NOT NULL,
    category TEXT NOT NULL
);
```

---

## ⚡ Tối Ưu Hóa Truy Vấn (Indexes)
Nhằm tăng hiệu năng tìm kiếm và lọc món ăn khi sinh viên tra cứu trên trang Web:
- **Chỉ mục mặc định**: SQLite tự động tạo chỉ mục trên cột khóa chính `id`.
- **Đề xuất chỉ mục phụ** (Khi dữ liệu mở rộng lớn hơn):
  - Tìm kiếm theo danh mục và giá:
    ```sql
    CREATE INDEX idx_foods_category_price ON foods(category, price);
    ```
  - Tìm kiếm theo tên (Case-insensitive LIKE):
    ```sql
    CREATE INDEX idx_foods_name ON foods(name);
    ```

---

## 📊 Phân Bổ Món Ăn Mẫu (Seeding Summary)
Script [database/seed.py](file:///Users/thien/Documents/learn/TDTKDMST/database/seed.py) nạp sẵn 115 món ăn gồm:
- **Bữa sáng**: 26 món (Bánh mì các loại, Phở, Bún riêu, Xôi, Cháo, Yến mạch...)
- **Bữa trưa / tối**: 50 món (Cơm tấm sườn bì chả, Cơm ba chỉ kho, Cơm đậu hũ dồn thịt, Bún thịt nướng, Nui xào bò...)
- **Bữa phụ (Ăn vặt)**: 21 món (Trứng gà luộc, Khoai lang, Bắp ngô luộc, Gỏi cuốn, Sữa chua nếp cẩm, Hạt điều...)
- **Nước uống**: 18 món (Sữa đậu nành UTH, Sinh tố bơ, Nước mía tắc, Cà phê sữa đá, Trà tắc mật ong...)

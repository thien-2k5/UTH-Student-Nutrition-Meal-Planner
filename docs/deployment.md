# Hướng Dẫn Triển Khai Ứng Dụng (Deployment Guide)
> **UTH Student Nutrition Meal Planner**

Tài liệu này cung cấp hướng dẫn triển khai ứng dụng web lên các dịch vụ điện toán đám mây (Cloud platforms) phổ biến hoặc chạy container hóa bằng Docker.

---

## 🌐 Live Demo Trên Azure

**Ứng dụng hiện đang chạy trên Azure VM:**

🔗 **URL Live:** `http://20.89.105.76:5001`

- **IP Address**: 20.89.105.76
- **Port**: 5001
- **Environment**: Production (Docker container)
- **Platform**: Azure Virtual Machine

### Các trang khả dụng:
- `/` - Trang chủ
- `/bmi` - Tính chỉ số BMI & TDEE
- `/recommend` - Gợi ý thực đơn theo ngân sách
- `/chat` - Chatbot hỗ trợ 24/7
- `/knowledge` - Cẩm nang kiến thức dinh dưỡng
- `/about` - Thông tin về dự án

---

## 🐋 1. Triển Khai Bằng Docker (Docker Deployment)

Bạn có thể chạy ứng dụng bằng cách đóng gói nó thành một Docker Container.

### Tệp `Dockerfile` đề xuất (Đặt tại thư mục gốc dự án):
```dockerfile
# Sử dụng Python image chính thức gọn nhẹ
FROM python:3.12-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Chạy lệnh nạp dữ liệu database
RUN python database/seed.py

# Khai báo cổng chạy ứng dụng
EXPOSE 5001

# Thiết lập biến môi trường chạy sản phẩm
ENV FLASK_ENV=production
ENV FLASK_RUN_PORT=5001

# Chạy ứng dụng bằng gunicorn phục vụ môi trường Production
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
```

### Lệnh xây dựng và khởi chạy:
```bash
# Xây dựng Docker Image
docker build -t uth-nutrition-planner .

# Chạy Docker Container
docker run -p 5001:5001 --env-file .env uth-nutrition-planner
```

---

## ⚡ 2. Triển Khai Lên Azure Virtual Machine (Hiện Tại)

### Yêu cầu
- Tài khoản Azure với đủ credit
- Azure CLI hoặc Azure Portal

### Các bước triển khai:

#### 1. Tạo Virtual Machine
```bash
# Tạo Resource Group
az group create --name uth-nutrition-rg --location southeastasia

# Tạo VM với Ubuntu 22.04
az vm create \
  --resource-group uth-nutrition-rg \
  --name uth-nutrition-vm \
  --image UbuntuLTS \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard
```

#### 2. Mở cổng trên Network Security Group
```bash
# Cho phép traffic cổng 5001
az vm open-port --resource-group uth-nutrition-rg \
  --name uth-nutrition-vm \
  --port 5001 \
  --priority 1001
```

#### 3. SSH vào VM và cài đặt ứng dụng
```bash
# SSH vào VM
ssh -i ~/.ssh/id_rsa azureuser@<VM_PUBLIC_IP>

# Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# Cài đặt Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Clone dự án
git clone <repository-url>
cd UTH-Student-Nutrition-Meal-Planner

# Xây dựng và chạy ứng dụng bằng Docker Compose
docker compose up -d --build

# Kiểm tra trạng thái
docker compose ps
```

#### 4. Truy cập ứng dụng
Ứng dụng sẽ chạy tại: `http://<VM_PUBLIC_IP>:5001`

**Ví dụ:** `http://20.89.105.76:5001`

#### 5. Thiết lập Nginx Reverse Proxy (Tùy chọn)
Để cải thiện hiệu suất và bảo mật:
```bash
# Cài đặt Nginx
sudo apt install nginx -y

# Cấu hình Nginx làm reverse proxy
sudo nano /etc/nginx/sites-available/default
```

Thêm nội dung:
```nginx
server {
    listen 80 default_server;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Khởi động lại Nginx:
```bash
sudo systemctl restart nginx
```

### Chi phí
- **Standard_B2s**: ~$38/tháng
- **Public IP**: ~$3/tháng
- **Total**: ~$41/tháng

---

## ☁️ 3. Triển Khai Lên Render (Render.com)

Render là dịch vụ Cloud App Hosting miễn phí/giá rẻ rất thích hợp cho các dự án Python/Flask.

1. **Kết nối kho lưu trữ**: Đẩy mã nguồn dự án lên GitHub và kết nối tài khoản GitHub của bạn với Render.
2. **Tạo Web Service**:
   - Chọn **New** -> **Web Service**.
   - Chọn kho lưu trữ dự án.
3. **Cấu hình thông tin dịch vụ**:
   - **Language**: `Python`
   - **Branch**: `main`
   - **Build Command**: Cài đặt dependencies và chạy seeding database:
     ```bash
     pip install -r requirements.txt && python database/seed.py
     ```
   - **Start Command**: Chạy ứng dụng bằng Gunicorn trên port 5001:
     ```bash
     gunicorn --bind 0.0.0.0:5001 app:app
     ```
4. **Environment Variables**: Thiết lập các biến môi trường trong phần **Env**:
   - `SECRET_KEY`: Khóa bảo mật ngẫu nhiên của bạn.
   - `GEMINI_API_KEY`: (Tùy chọn) Khóa API Google Gemini để chạy AI chatbot.
   - `FLASK_ENV`: `production`

---

## 🚂 4. Triển Khai Lên Railway (Railway.app)

Railway cung cấp tốc độ triển khai ứng dụng cực nhanh và tự động hóa cao.

1. Cài đặt công cụ CLI của Railway hoặc liên kết trực tiếp tài khoản GitHub của bạn.
2. Tạo dự án mới trên giao diện Railway và liên kết Repo dự án.
3. **Cơ chế phát hiện tự động**: Railway sẽ tự phát hiện dự án Flask nhờ tệp `requirements.txt` và `app.py`.
4. Thiết lập biến môi trường (`SECRET_KEY`, `GEMINI_API_KEY`) trên Dashboard Railway.
5. Railway sẽ tự động triển khai dựa vào tệp `Procfile` nếu có, hoặc bạn có thể chỉ định lệnh khởi chạy trong cài đặt:
   `gunicorn --bind 0.0.0.0:5001 app:app`

---

## 🐍 5. Triển Khai Lên PythonAnywhere

Dịch vụ hosting chuyên dụng cho Python.

1. Đăng ký tài khoản miễn phí trên [PythonAnywhere](https://www.pythonanywhere.com/).
2. Mở một **Bash Console** và clone project từ GitHub hoặc tải file zip lên.
3. Tạo môi trường ảo và cài đặt thư viện:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.12 uth-env
   pip install -r requirements.txt
   python database/seed.py
   ```
4. Vào trang quản lý **Web** và chọn **Add a new web app**:
   - Chọn **Manual Configuration** -> Chọn phiên bản **Python 3.10/3.11/3.12**.
5. Cấu hình đường dẫn Web App trên Dashboard:
   - **Source code**: Đường dẫn thư mục dự án (e.g. `/home/username/TDTKDMST`).
   - **Working directory**: Đường dẫn thư mục dự án.
   - **Virtualenv**: Đường dẫn tới virtualenv vừa tạo (e.g. `/home/username/.virtualenvs/uth-env`).
6. Cấu hình tệp WSGI bằng cách nhấp vào link `WSGI configuration file` trên Dashboard và sửa nội dung thành:
   ```python
   import sys
   import os

   path = '/home/username/TDTKDMST' # Thay bằng tên đăng nhập của bạn
   if path not in sys.path:
       sys.path.append(path)

   from app import app as application
   ```
7. Nhấn **Reload** để chạy ứng dụng của bạn.

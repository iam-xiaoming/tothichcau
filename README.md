# Web bán key game trực tuyến

## Giới thiệu

Trang web bán key game trực tuyến, tích hợp thanh toán, xác thực người dùng, và quản lý đơn hàng.

---

## Công nghệ chính

| Công nghệ               | Mô tả                                   |
| ----------------------- | --------------------------------------- |
| Django                  | Framework Python mạnh mẽ, dễ triển khai |
| PostgreSQL + Aiven      | Cơ sở dữ liệu quan hệ mạnh mẽ           |
| Stripe                  | Thanh toán quốc tế qua API REST         |
| Amazon S3               | Lưu trữ media (ảnh, video review)       |
| Firebase Authentication | Đăng nhập OAuth2, OTP, email            |
| Elasticsearch           | Tìm kiếm toàn văn, autocomplete         |
| Redis                   | Cache và message broker cho Celery      |
| Celery                  | Xử lý tác vụ nền                        |

---

## Tính năng chính

- Quản lý game, DLC, danh mục (CRUD)
- Thanh toán & giỏ hàng (Stripe Checkout + webhook)
- Xác thực người dùng (Firebase)
- Đánh giá & bình luận game
- Lưu trữ và hiển thị media review (ảnh, video)

---

## Hướng dẫn cài đặt

### 1. Clone repo

```bash
git clone https://github.com/xiaoMing-04/CoDaiVaHoaDanhDanh.git
cd CoDaiVaHoaDanhDanh
````

### 2. Lấy file `.env`

*Liên hệ nhóm phát triển để nhận file cấu hình `.env`.*

### 3. Chạy với Docker (Windows/Mac/Linux)

#### a) Cài Docker Desktop (Windows/Mac) hoặc Docker Engine (Linux)

* [Docker Desktop cho Windows/Mac](https://www.docker.com/products/docker-desktop/)

#### b) Pull image Docker

```bash
docker pull nguyenminh079/game-art:v1.0
docker pull redis:7-alpine
```

#### c) Tạo file `docker-compose.yml` (hoặc dùng file có sẵn) với nội dung:

```yaml
version: "3.9"
services:
  django:
    image: nguyenminh079/game-art:v1.0
    ports:
      - "8000:8000"
    command: gunicorn GameArt.wsgi:application --bind 0.0.0.0:8000 --timeout 120
    depends_on:
      - redis

  celery:
    image: nguyenminh079/game-art:v1.0
    command: celery -A GameArt worker --loglevel=info
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
```

#### d) Chạy Docker Compose

```bash
docker compose up -d
```

### 4. Chạy trên máy không dùng Docker (tuỳ chọn, cần Python và môi trường ảo)

```bash
python -m venv venv
source venv/bin/activate    # trên Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

---

## Liên hệ nhóm thực hiện

| Họ Tên           | MSSV     |
| ---------------- | -------- |
| Trần Thị Huyền   | 22657821 |
| Nguyễn Ngọc Minh | 22685841 |
| Phan Công Chiến  | 22685651 |
| Trần Thái Nguyên (Nguyn thich xem sexual content) | 22697051 |
| Trần Khắc Liêm   | 22685251 |

```
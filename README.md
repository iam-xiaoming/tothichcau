# Web bán key game trực tuyến

## Giới thiệu

Trang web bán key game trực tuyến, tích hợp thanh toán, xác thực người dùng, và quản lý đơn hàng.

---

## Mục Lục

- [Giới thiệu](#giới-thiệu)
- [Công nghệ chính](#công-nghệ-chính)
- [Tính năng chính](#tính-năng-chính)
- [Yêu cầu](#yêu-cầu)
- [Hướng dẫn cài đặt](#hướng-dẫn-cài-đặt)
- [Link triển khai](#link-triển-khai)
- [Liên hệ nhóm thực hiện](#liên-hệ-nhóm-thực-hiện)

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
| Mailjet                 | Xử lý gửi email khi giao dịch thành công|
| CloudFront              | Tăng tốc độ xử lý file tĩnh             |

---

## Tính năng chính

- Quản lý game, DLC, danh mục (CRUD)
- Thanh toán & giỏ hàng (Stripe Checkout + webhook)
- Xác thực người dùng (Firebase)
- Đánh giá & bình luận game
- Lưu trữ và hiển thị media review (ảnh, video)

---

## Yêu cầu

- Docker (>=20.x), Docker Compose (>=1.29.x)
- Python 3.11 (nếu chạy local)
- File `.env` với cấu hình môi trường đầy đủ (liên hệ nhóm phát triển)

---

## Hướng dẫn cài đặt

### 1. Clone repo

```bash
git clone https://github.com/xiaoMing-04/tothichcau.git
cd tothichcau
````

### 2. Lấy file `.env`

*Liên hệ nhóm phát triển để nhận file cấu hình `.env`.*

### 3. Chạy với Docker (Windows/Mac/Linux) (CPU kiến trúc ARM)
*Note: Chạy `docker-compose` hoặc `docker compose` tuỳ máy. Cách kiểm tra `docker-compose version`.*

```bash
docker-compose pull
docker-compose up -d
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

### 4. Chạy trên máy không dùng Docker (tuỳ chọn)

```bash
python -m venv venv
source venv/bin/activate    # trên Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Link triển khai (Deploy)

👉 **[https://www.tothichcau.shop/](https://www.tothichcau.shop/)**

---

## Liên hệ nhóm thực hiện

| Họ Tên           | MSSV     |
| ---------------- | -------- |
| Trần Thị Huyền   | 22657821 |
| Nguyễn Ngọc Minh | 22685841 |
| Phan Công Chiến  | 22685651 |
| Trần Thái Nguyên | 22697051 |
| Trần Khắc Liêm   | 22685251 |
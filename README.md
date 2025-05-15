<!-- localhost:8000/api/search/games/?query=elden&offset=0&limit=10 -->
### Link donate đây nha ae
<img src="donate.jpg" alt="Alt text" width="300">

Kênh chơi game với mục đích đem lại niềm vui cho mọi người: https://www.facebook.com/profile.php?id=100027733654960&mibextid=LQQJ4d


## 🎮 XÂY DỰNG TRANG WEB BÁN KEY GAME TRỰC TUYẾN

**Tích hợp thanh toán và xác thực người dùng**

**Nhóm thực hiện:**

| Họ Tên               | MSSV     |
| -------------------- | -------- |
| **Trần Thị Huyền**   | 22657821 |
| **Nguyễn Ngọc Minh** | 22685841 |
| **Phan Công Chiến**  | 22685651 |
| **Trần Thái Nguyên** | 22697051 |
| **Trần Khắc Liêm**   | 22685251 |

---

## 📑 MỤC LỤC

1. Giới thiệu công cụ & công nghệ
2. Tính năng chính
3. Hướng dẫn cài đặt & link code
4. Kiến trúc hệ thống
5. Demo & triển khai
6. Kết luận & hướng mở rộng

---

## 🔧 GIỚI THIỆU CÔNG NGHỆ

| Công cụ                     | Mô tả                                                                                 |
| --------------------------- | ------------------------------------------------------------------------------------- |
| **Django**                  | Framework Python mạnh mẽ, tích hợp ORM, admin, routing. Cộng đồng lớn, dễ triển khai. |
| **PostgreSQL + Aiven**      | CSDL quan hệ mạnh mẽ, backup tự động, sẵn sàng cao.                                   |
| **Stripe**                  | Thanh toán quốc tế qua API REST, hỗ trợ webhook gửi key.                              |
| **Amazon S3**               | Lưu trữ media (ảnh, video review), tích hợp qua `django-storages`.                    |
| **Firebase Authentication** | Đăng nhập OAuth2, OTP, email, triển khai nhanh, gói free.                             |
| **Elasticsearch**           | Tìm kiếm toàn văn, autocomplete, tùy chỉnh analyzer.                                  |
| **Crisp Chat**              | Hỗ trợ live chat, email bot, phân tích hành vi người dùng.                            |
| **AWS Personalize**         | Gợi ý game theo hành vi, không cần build ML từ đầu.                                   |
| **AWS CloudFront**          | CDN toàn cầu, tăng tốc S3, hỗ trợ cache, SSL.                                         |

---

## 🧩 TÍNH NĂNG CHÍNH

* **Đồng bộ dữ liệu**: Quản lý game, DLC, danh mục (CRUD)
* **Thanh toán & Giỏ hàng**: Stripe Checkout, xử lý webhook nhận key
* **Xác thực người dùng**: Firebase login, quản trị bằng Django admin
* **Đánh giá & Bình luận**: User comment, điểm số trung bình
* **Review Media**: Hình ảnh, video minh họa cho game

---

## 🖥️ DEMO GIAO DIỆN

* **Trang chủ**: Logo thương hiệu rõ ràng, giao diện dễ điều hướng
* **Trang chi tiết game**: Thông tin chi tiết, ảnh, video review
* **Giỏ hàng**: Quản lý đơn hàng, xác nhận thanh toán
* **Đánh giá người dùng**: Gửi comment, rating, hiển thị điểm trung bình

---

## ⚙️ HƯỚNG DẪN CÀI ĐẶT

**Repo GitHub:**
🔗 [https://github.com/xiaoMing-04/CoDaiVaHoaDanhDanh](https://github.com/xiaoMing-04/CoDaiVaHoaDanhDanh)

**Cấu trúc thư mục:**
`games/`, `users/`, `cart/`, ...

### Cài đặt local:
```bash
git clone ...
cd project/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Docker Compose (tuỳ chọn):

* Cho PostgreSQL, Redis, Elasticsearch
* File `docker-compose.yml`

```bash
docker-compose up -d
```

---

## 🏗️ KIẾN TRÚC HỆ THỐNG

**Luồng hoạt động:**

1. User đăng nhập qua Firebase
2. Giao diện frontend chọn game → thêm vào giỏ
3. Gửi thanh toán qua Stripe
4. Webhook trả key game → hiển thị/gửi mail

**Tổ chức Django:**

* `models.py`: Game, DLC, Rating
* `serializers.py`: Chuẩn hóa API
* `views.py`: API & Web (CBV/FBV)
* `signals.py`: Stripe webhook, tự động tính điểm

---

## 🚀 TRIỂN KHAI & DEMO

**Deploy tại:** \[Render.com]

* Tự động deploy từ GitHub
* Domain HTTPS
* Thiết lập môi trường `.env`

### Demo quy trình:

1. Đăng ký user
2. Chọn game → Thêm vào giỏ
3. Thanh toán bằng Stripe (test card)
4. Hệ thống trả key → hiển thị/sent email

---

## ✅ KẾT LUẬN

* Hoàn thành MVP hệ thống bán key game
* Dễ dàng triển khai, tích hợp dịch vụ hiện đại
* Hỗ trợ mở rộng cả backend và frontend

---

## 🔮 HƯỚNG MỞ RỘNG

* Đa dạng cách thức đăng ký
* Tích hợp API nhà cung cấp key tự động
* Gợi ý game theo sở thích người dùng (AWS Personalize)
* Giao diện mobile bằng **React Native**
* Phát triển cộng đồng user: comment, vote, review


### Một số lỗi hay gặp
1. chạy là lỗi gì liên quan tới aws hay trong app recommender thì là do chưa xác thực aws cli, hãy xác thực aws cli, xong nó yêu cầu nhập acccess key và secret key và region thì nó trong file env. mấy các khác thì enter để bỏ qua.
2. `pull origin main` không đc thì chạy `git reset --hard HEAD`, xong pull lại. nếu không thấy cập nhật gì thì đóng hết mấy file đang mở.
3. lỗi: đổi tên db trong file .env hay hay thay đổi trong settings.py nó vẫn load cái cũ, không cập nhật cái mới (cách để biết cũ hay mới là vào settings.py dùng lệnh `print` ra rồi `runserver` để xem nó in ra terminal cái gì), thì đóng hết tất cả các terminal, xong bật lại cái mới

### Cách chạy
1. clone về
2. xin file env
3. mở docker desktop, chạy `docker compose up` nếu muốn sử dụng tính năng search, nếu không hãy vào settings.py, INSTALLED_APPS và comment `django_elasticsearch_dsl` lại, nếu không, thêm hoặc chỉnh sửa sẽ lỗi. còn nếu muốn dùng search, sau khi docker compose up, chạy `python3 manage.py search_index --rebuild`
4. Nếu muốn lưu file ảnh/video trên máy, thì vào settings.py DEBUG = True, không thì False. nếu DEBUG = False, thì sau đó chạy `python3 manage.py collectstatic`, nó hỏi thì ấn `yes`, rồi `runserver`, sau đó vào Chrome, nhấn Ctrl + Shift + R (Window) hoặc Cmd + Option + R (Mac) để nó xóa cache (file js, css còn lưu ở cache) (nếu đéo thấy gì thay đổi thì ấn tiếp 2 3 lần nữa)

5. chạy `py manage.py makemigrations`
6. chạy `py manage.py migrate`

7. khúc `makemigrations`, `migrate` mà lỗi kiểu như `column xxx and relation yyy already exist....` thì xóa hết file migrations, xóa như nào thì hỏi chatgpt. sau khi xóa nếu chạy lỗi `no module` cái đéo gì đó thì `pip uninstall Django` ->  `pip install Django`. còn nếu lỗi nữa thì lên Aiven xóa database tạo lại cái mới

7. run `python3 manage.py createsuperuser` để tạo tài khoản admin
6. chạy `py manage.py runserver`


8. nếu DEBUG = False, khi ảnh/video/css/js.... sẽ lưu trên aws. truy cập `https://396913705803.signin.aws.amazon.com/console`, tk: `hoangtuthieutien`, mk: `nothingsgonnachangemyloveforyou-2`; chỗ thanh tìm kiếm, gõ chữ `S3` rồi nhấn vào `S3`. và chọn bucket ứng với tên `AWS_STORAGE_BUCKET_NAME` trong file .env, 

9. Nếu muốn dùng tính năng thanh toán chạy `stripe listen --forward-to localhost:8000/webhook/stripe/`, nếu không sẽ bị lỗi. stripe webhook cần phải cài stripe cli, chứ đéo phải cài mỗi cái thư viện stripe là đủ ok. còn cài thế nào thì lên youtube. cài xong thì chạy `stripe login`, phải login, đéo biết thì hỏi chatgpt. cái tài khoản stripe login này phải là cái tài khoản trùng với tài khoản đc thêm vào project, nếu không sẽ bị lỗi.


<!-- export VISUAL=nano

crontab -e

crontab -l

*/10 * * * * /Users/nguyenminh/Mac/CoDaiVaHoaDanhDanh/venv/bin/python /Users/nguyenminh/Mac/CoDaiVaHoaDanhDanh/manage.py release_expired_orders >> /Users/nguyenminh/Mac/CoDaiVaHoaDanhDanh/logs/cron_release.log 2>&1

*/3 * * * * echo "Cron job ran at $(date)" >> /Users/nguyenminh/Mac/CoDaiVaHoaDanhDanh/logs/test_cron.log 2>&1

api/dlc/3/media/review/ -->

redis-server
redis-cli ping
python manage.py migrate django_celery_beat
celery -A GameArt worker --loglevel=info --logfile=celery.log
celery -A GameArt beat --loglevel=info


docker compose up --build

<!-- docker compose build
docker compose up -->

docker compose exec django python manage.py makemigrations
docker compose exec django python manage.py migrate

docker tag codaivahoadanhdanh-django:latest babyshark04/gameart:latest
docker push babyshark04/gameart:latest

<!-- pulll and run -->
docker pull babyshark04/gameart-django:latest
docker pull babyshark04/gameart-celery:latest

docker compose up
tranthihuyenaaaaa@gmail.com
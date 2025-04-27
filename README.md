<!-- localhost:8000/api/search/games/?query=elden&offset=0&limit=10 -->


<!-- Kênh chơi game với mục đích đem lại niềm vui cho mọi người: https://www.facebook.com/profile.php?id=100027733654960&mibextid=LQQJ4d -->


<!-- find . -path "*/migrations/*.py" -not -name "__init__.py" -delete -->

<!-- find . -path "*/migrations/*.pyc" -delete -->

### Running tutorial
0. `pull origin main` không đc thì chạy `git reset --hard HEAD`, xong pull lại. nếu không thấy cập nhật gì thì đóng hết mấy file đang mở.
0. lỗi: đổi tên db trong file .env hay đổi cái đéo gì cũng đc mà trong settings.py nó vẫn load cái cũ, ko cập nhật cái mới (cách để biết cũ hay mới là vào settings.py dùng lệnh `print` ra rồi `runserver` để xem nó in ra terminal là cái đéo gì), thì đóng hết tất cả các terminal, xong bật lại cái mới

1. clone về
2. xin file env
3. mở docker desktop, chạy `docker compose up` nếu muốn sử dụng tính năng search, nếu không hãy vào settings.py, INSTALLED_APPS và comment `django_elasticsearch_dsl` lại, nếu không, thêm hoặc chỉnh sửa sẽ lỗi. còn nếu muốn dùng search, sau khi docker compose up, chạy `python3 manage.py search_index --rebuild`
4. Nếu muốn lưu file ảnh/video trên máy, thì vào settings.py DEBUG = True, không thì False. nếu DEBUG = False, thì sau đó chạy `python3 manage.py collectstatic`, nó hỏi thì ấn `yes`, rồi `runserver`, sau đó vào Chrome, nhấn Ctrl + Shift + R (Window) hoặc Cmd + Option + R (Mac) (nếu đéo thấy gì thay đổi thì ấn tiếp 2 3 lần nữa)

5. chạy `py manage.py makemigrations`
6. chạy `py manage.py migrate`

10. khúc `5`, `6` mà lỗi thì xóa hết file migrations, xóa như nào thì hỏi chatgpt. sau khi xóa nếu chạy lỗi `no module` cái đéo gì đó thì `pip uninstall Django` ->  `pip install Django`. còn nếu lỗi nữa thì lên Aiven xóa database tạo lại cái mới

7. run `python3 manage.py createsuperuser` để tạo tài khoản admin
6. chạy `py manage.py runserver`


8. nếu DEBUG = False, khi ảnh/video/css/js.... sẽ lưu trên aws. truy cập `https://396913705803.signin.aws.amazon.com/console`, tk: `hoangtuthieutien`, mk: `nothingsgonnachangemyloveforyou-2`; chỗ thanh tìm kiếm, gõ chữ `S3` rồi nhấn vào `S3`. và chọn bucket ứng với tên `AWS_STORAGE_BUCKET_NAME` trong file .env, 

9. Nếu muốn dùng tính năng thanh toán chạy `stripe listen --forward-to localhost:8000/webhook/stripe/`, nếu không sẽ bị lỗi. stripe webhook cần phải cài stripe cli, chứ đéo phải cài mỗi cái thư viện stripe là đủ ok. còn cài thế nào thì lên youtube. cài xong thì chạy `stripe login`, phải login, đéo biết thì hỏi chatgpt. cái tài khoản stripe login này phải là cái tài khoản trùng với tài khoản đc thêm vào project, nếu không sẽ bị lỗi.


export VISUAL=nano

crontab -e

crontab -l

*/10 * * * * /Users/nguyenminh/Mac/CoDaiVaHoaDanhDanh/venv/bin/python /Users/nguyenminh/Mac/CoDaiVaHoaDanhDanh/manage.py release_expired_orders >> /Users/nguyenminh/Mac/CoDaiVaHoaDanhDanh/logs/cron_release.log 2>&1

*/3 * * * * echo "Cron job ran at $(date)" >> /Users/nguyenminh/Mac/CoDaiVaHoaDanhDanh/logs/test_cron.log 2>&1
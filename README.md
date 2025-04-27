docker compose up

stripe listen --forward-to localhost:8000/webhook/stripe/

python3 manage.py runserver

localhost:8000/api/search/games/?query=elden&offset=0&limit=10


Kênh chơi game với mục đích đem lại niềm vui cho mọi người: https://www.facebook.com/profile.php?id=100027733654960&mibextid=LQQJ4d


https://396913705803.signin.aws.amazon.com/console

hoangtuthieutien

nothingsgonnachangemyloveforyou-2

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

find . -path "*/migrations/*.pyc" -delete

### Running tutorial

1. clone về
2. xin file env
3. mở docker desktop
4. chạy `docker compose up`
5. run `python3 manage.py search_index --rebuild` (optional)
5. chạy `py manage.py makemigrations`
6. chạy `py manage.py migrate`
6. chạy `py manage.py runserver`


export VISUAL=nano

crontab -e

crontab -l

*/10 * * * * /Users/nguyenminh/Mac/CoDaiVaHoaDanhDanh/venv/bin/python /Users/nguyenminh/Mac/CoDaiVaHoaDanhDanh/manage.py release_expired_orders >> /Users/nguyenminh/Mac/CoDaiVaHoaDanhDanh/logs/cron_release.log 2>&1


*/3 * * * * echo "Cron job ran at $(date)" >> /Users/nguyenminh/Mac/CoDaiVaHoaDanhDanh/logs/test_cron.log 2>&1
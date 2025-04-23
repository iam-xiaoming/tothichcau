docker compose up

stripe listen --forward-to localhost:8000/webhook/stripe/

python3 manage.py runserver

localhost:8000/api/search/games/?query=elden&offset=0&limit=10

python3 manage.py search_index --rebuild


Kênh chơi game với mục đích đem lại niềm vui cho mọi người: https://www.facebook.com/profile.php?id=100027733654960&mibextid=LQQJ4d
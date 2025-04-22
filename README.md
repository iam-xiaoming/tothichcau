docker compose up

stripe listen --forward-to localhost:8000/webhook/stripe/

python3 manage.py runserver
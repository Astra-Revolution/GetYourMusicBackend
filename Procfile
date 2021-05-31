release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
web: gunicorn GetYourMusic.asgi
worker: python manage.py runworker channel_layer
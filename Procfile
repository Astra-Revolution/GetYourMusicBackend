release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
web: gunicorn GetYourMusic.wsgi
worker: python manage.py runworker channel_layer
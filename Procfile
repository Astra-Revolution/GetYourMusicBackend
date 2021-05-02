release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
web: gunicorn otorongo_back_end.wsgi
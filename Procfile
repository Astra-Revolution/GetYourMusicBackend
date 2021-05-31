release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
release: export DJANGO_SETTINGS_MODULE=GetYourMusic.settings
web: daphne GetYourMusic.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer --settings=GetYourMusic.settings -v2
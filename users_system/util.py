import secrets

from django.conf import settings
from django.core.mail import send_mail


def generate_token():
    return secrets.token_urlsafe(20)


def send_email(user):
    subject = 'Forgot password'
    link = f'http://127.0.0.1:3000/?token={user.aux_token}'
    message = f'Please, click the link to restore your password: {link}'
    email_from = settings.EMAIL_HOST_USER
    users_list = [user.email]
    send_mail(subject, message, email_from, users_list)


def reset_aux_token(user):
    user.aux_token = None
    user.save()

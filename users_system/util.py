from django.conf import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


def generate_token(user):
    token = RefreshToken.for_user(user).access_token
    return str(token)


def send_email(recipients, subject, message):
    send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipients)

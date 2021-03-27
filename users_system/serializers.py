from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_password(value: str) -> str:
        return make_password(value)

    # def create(self, validated_data):
    #     user = User.objects.create(**validated_data)
    #     if not user:
    #         raise Exception("Error creating user")
    #     email = validated_data['email']
    #     subject = 'Thank you for registering to  our site'
    #     message = ' it  means a world to us '
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list = [email]
    #     send_mail(subject, message, email_from, recipient_list)
    #     return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

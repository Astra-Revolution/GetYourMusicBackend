from rest_framework import serializers

from social_media.models import Following
from .models import User, Profile, Musician, Organizer
from locations.models import District
from datetime import date
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


class ProfileSerializer(serializers.ModelSerializer):
    district_id = serializers.IntegerField(write_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)

    def create(self, validated_data):
        user = User.objects.get(id=validated_data["user_id"])
        validated_data["user"] = user
        district = District.objects.get(id=validated_data["district_id"])
        validated_data["district"] = district
        validated_data["register_date"] = str(date.today())
        validated_data["type"] = validated_data["type"].lower()
        profile = None
        if validated_data["type"] == "musician":
            profile = Musician.objects.create(**validated_data)
        elif validated_data["type"] == "organizer":
            profile = Organizer.objects.create(**validated_data)
        return profile

    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'last_name', 'birth_date', 'phone',
                  'image_url', 'type', 'register_date', 'user_email', 'district_name', 'district_id')
        read_only_fields = ('register_date', 'user')


class MusicianSerializer(ProfileSerializer):
    followers = serializers.SerializerMethodField('get_followers', read_only=True)
    followed = serializers.SerializerMethodField('get_followed', read_only=True)

    @staticmethod
    def get_followers(self):
        followers = Following.objects.filter(followed_id=self.pk)
        return followers.count()

    @staticmethod
    def get_followed(self):
        followers = Following.objects.filter(follower_id=self.pk)
        return followers.count()

    class Meta:
        model = Musician
        fields = ProfileSerializer.Meta.fields + ('rating', 'artistic_name', 'followers', 'followed')


class OrganizerSerializer(ProfileSerializer):
    class Meta:
        model = Organizer
        fields = ProfileSerializer.Meta.fields

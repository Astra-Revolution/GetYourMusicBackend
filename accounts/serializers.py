from rest_framework import serializers

from social_media.models import Following
from .models import User, Profile, Musician, Organizer
from datetime import date
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_password(value: str) -> str:
        return make_password(value)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)

    def create(self, validated_data):
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
        fields = ('user', 'first_name', 'last_name', 'birth_date', 'phone', 'image_url',
                  'type', 'register_date', 'user_email', 'district_name')
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

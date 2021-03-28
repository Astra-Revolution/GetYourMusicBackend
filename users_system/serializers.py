from rest_framework import serializers
from .models import User, Profile, Musician, Organizer, Following
from locations.models import District
from datetime import date
from django.contrib.auth.hashers import make_password
import social_system.notifier


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
        typeProfile = validated_data["type"]
        profile = None
        if typeProfile == "Musician":
            profile = Musician.objects.create(**validated_data)
        elif typeProfile == "Organizer":
            profile = Organizer.objects.create(**validated_data)
        return profile

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'birth_date', 'phone',
                'type', 'register_date', 'user_email', 'district_name', 'district_id')
        read_only_fields = ('register_date',)


class MusicianSerializer(ProfileSerializer):
    class Meta:
        model = Musician
        fields = ProfileSerializer.Meta.fields + ('rating', 'artistic_name')


class OrganizerSerializer(ProfileSerializer):
    class Meta:
        model = Organizer
        fields = ProfileSerializer.Meta.fields


class FollowingSerializer(serializers.ModelSerializer):
    follower_name = serializers.CharField(source='follower.first_name', read_only=True)
    followed_name = serializers.CharField(source='followed.first_name', read_only=True)

    def create(self, validated_data):
        follower = Musician.objects.get(id=validated_data["follower_id"])
        validated_data["follower"] = follower
        followed = Musician.objects.get(id=validated_data["followed_id"])
        validated_data["followed"] = followed
        validated_data["follow_date"] = str(date.today())
        following = Following.objects.create(**validated_data)
        social_system.notifier.notifier(following)
        return following

    class Meta:
        model = Following
        fields = ('follower_name', 'followed_name', 'follow_date')
        read_only_fields = ('follow_date',)

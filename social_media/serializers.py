from rest_framework import serializers
from datetime import date
from .models import Publication, Comment, Notification, Following, Genre, Instrument
from accounts.models import Profile, Musician
import social_media.notifier


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ('id', 'name')


class PublicationSerializer(serializers.ModelSerializer):
    musician_id = serializers.IntegerField(source='musician.user.id', read_only=True)
    musician_name = serializers.SerializerMethodField('get_full_name', read_only=True)

    @staticmethod
    def get_full_name(self):
        musician = self.musician
        full_name = f'{musician.first_name} {musician.last_name}'
        return full_name

    def create(self, validated_data):
        musician = Musician.objects.get(user=validated_data["musician_id"])
        validated_data["musician"] = musician
        validated_data["update_time"] = str(date.today())
        publication = Publication.objects.create(**validated_data)
        return publication

    class Meta:
        model = Publication
        fields = ('id', 'video_url', 'content', 'update_time', 'musician_id', 'musician_name')
        read_only_fields = ('update_time',)


class CommentSerializer(serializers.ModelSerializer):
    commenter_id = serializers.IntegerField(source='commenter.user.id', read_only=True)
    commenter_name = serializers.SerializerMethodField('get_full_name', read_only=True)
    commenter_image = serializers.CharField(source='commenter.image_url', read_only=True)
    content = serializers.CharField(source='publication.content', read_only=True)

    @staticmethod
    def get_full_name(self):
        musician = self.commenter
        full_name = f'{musician.first_name} {musician.last_name}'
        return full_name

    def create(self, validated_data):
        commenter = Profile.objects.get(user=validated_data["commenter_id"])
        validated_data["commenter"] = commenter
        publication = Publication.objects.get(id=validated_data["publication_id"])
        validated_data["publication"] = publication
        comment = Comment.objects.create(**validated_data)
        social_media.notifier.notifier(comment)
        return comment

    class Meta:
        model = Comment
        fields = ('id', 'text', 'commenter_id', 'commenter_name', 'commenter_image', 'content')


class FollowingSerializer(serializers.ModelSerializer):
    follower_name = serializers.CharField(source='follower.first_name', read_only=True)
    followed_name = serializers.CharField(source='followed.first_name', read_only=True)

    def create(self, validated_data):
        follower = Musician.objects.get(user=validated_data["follower_id"])
        validated_data["follower"] = follower
        followed = Musician.objects.get(user=validated_data["followed_id"])
        validated_data["followed"] = followed
        validated_data["follow_date"] = str(date.today())
        following = Following.objects.create(**validated_data)
        social_media.notifier.notifier(following)
        return following

    class Meta:
        model = Following
        fields = ('follower_name', 'followed_name', 'follow_date')
        read_only_fields = ('follow_date',)


class FollowerSerializer(serializers.ModelSerializer):
    musician_id = serializers.IntegerField(source='follower.user.id', read_only=True)
    musician_name = serializers.SerializerMethodField('get_full_name', read_only=True)
    musician_image = serializers.CharField(source='follower.image_url', read_only=True)
    followers = serializers.SerializerMethodField('get_followers', read_only=True)

    @staticmethod
    def get_full_name(self):
        musician = self.follower
        full_name = f'{musician.first_name} {musician.last_name}'
        return full_name

    @staticmethod
    def get_followers(self):
        followers = Following.objects.filter(followed_id=self.followed)
        return followers.count()

    class Meta:
        model = Following
        fields = ('musician_id', 'musician_name', 'musician_image', 'followers', 'follow_date')
        read_only_fields = ('follow_date',)


class FollowedSerializer(serializers.ModelSerializer):
    musician_id = serializers.IntegerField(source='followed.user.id', read_only=True)
    musician_name = serializers.SerializerMethodField('get_full_name', read_only=True)
    musician_image = serializers.CharField(source='followed.image_url', read_only=True)
    followers = serializers.SerializerMethodField('get_followers', read_only=True)

    @staticmethod
    def get_full_name(self):
        musician = self.followed
        full_name = f'{musician.first_name} {musician.last_name}'
        return full_name

    @staticmethod
    def get_followers(self):
        followers = Following.objects.filter(followed_id=self.follower)
        return followers.count()

    class Meta:
        model = Following
        fields = ('musician_id', 'musician_name', 'musician_image', 'followers', 'follow_date')
        read_only_fields = ('follow_date',)


class NotificationSerializer(serializers.ModelSerializer):
    profile_name = serializers.CharField(source='profile.first_name', read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'message', 'created_at', 'profile_name')
        read_only_fields = ('created_at',)

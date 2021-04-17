from rest_framework import serializers
from datetime import date
from .models import Publication, Comment, Notification, Following, Genre, Instrument
from users_system.models import Profile, Musician
import social_media_system.notifier


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ('id', 'name')


class PublicationSerializer(serializers.ModelSerializer):
    musician_name = serializers.CharField(source='musician.first_name', read_only=True)

    def create(self, validated_data):
        musician = Musician.objects.get(user=validated_data["musician_id"])
        validated_data["musician"] = musician
        validated_data["update_time"] = str(date.today())
        publication = Publication.objects.create(**validated_data)
        return publication

    class Meta:
        model = Publication
        fields = ('id', 'video_url', 'content', 'update_time', 'musician_name')
        read_only_fields = ('update_time',)


class CommentSerializer(serializers.ModelSerializer):
    commenter_name = serializers.CharField(source='commenter.first_name', read_only=True)
    content = serializers.CharField(source='publication.content', read_only=True)

    def create(self, validated_data):
        commenter = Profile.objects.get(user=validated_data["commenter_id"])
        validated_data["commenter"] = commenter
        publication = Publication.objects.get(id=validated_data["publication_id"])
        validated_data["publication"] = publication
        comment = Comment.objects.create(**validated_data)
        social_media_system.notifier.notifier(comment)
        return comment

    class Meta:
        model = Comment
        fields = ('id', 'text', 'commenter_name', 'content')


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
        social_media_system.notifier.notifier(following)
        return following

    class Meta:
        model = Following
        fields = ('follower_name', 'followed_name', 'follow_date')
        read_only_fields = ('follow_date',)


class NotificationSerializer(serializers.ModelSerializer):
    profile_name = serializers.CharField(source='profile.first_name', read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'message', 'profile_name')

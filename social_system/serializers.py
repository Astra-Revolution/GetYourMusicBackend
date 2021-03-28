from rest_framework import serializers
from datetime import date
from .models import Publication, Comment
from users_system.models import Profile, Musician


class PublicationSerializer(serializers.ModelSerializer):
    musician_name = serializers.CharField(source='musician.first_name', read_only=True)

    def create(self, validated_data):
        musician = Musician.objects.get(id=validated_data["musician_id"])
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
        commenter = Profile.objects.get(id=validated_data["commenter_id"])
        validated_data["commenter"] = commenter
        publication = Publication.objects.get(id=validated_data["publication_id"])
        validated_data["publication"] = publication
        comment = Comment.objects.create(**validated_data)
        return comment

    class Meta:
        model = Comment
        fields = ('id', 'text', 'commenter_name', 'content')

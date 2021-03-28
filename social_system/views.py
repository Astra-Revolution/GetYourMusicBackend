from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *
from .serializers import PublicationSerializer, CommentSerializer, NotificationSerializer
from .models import Publication, Comment, Notification
from users_system.models import Profile, Musician

publications_response = openapi.Response('publications description', PublicationSerializer(many=True))
publication_response = openapi.Response('publication description', PublicationSerializer)
comments_response = openapi.Response('comments description', CommentSerializer(many=True))
comment_response = openapi.Response('comment description', CommentSerializer)
notifications_response = openapi.Response('notifications description', NotificationSerializer(many=True))


@swagger_auto_schema(method='get', responses={200: publications_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def publication_list(request):
    if request.method == 'GET':
        publications = Publication.objects.all()
        serializer = PublicationSerializer(publications, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: publications_response})
@swagger_auto_schema(methods=['post'], request_body=PublicationSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def musician_publications(request, musician_id):
    if request.method == 'GET':
        publications = Publication.objects.filter(musician__id=musician_id)
        serializer = PublicationSerializer(publications, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        try:
            Musician.objects.get(id=musician_id)
        except Musician.DoesNotExist:
            raise Http404

        serializer = PublicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(musician_id=musician_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: publication_response})
@swagger_auto_schema(methods=['put'], request_body=PublicationSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def publication_detail(request, publication_id):
    try:
        publication = Publication.objects.get(id=publication_id)
    except Publication.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = PublicationSerializer(publication)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PublicationSerializer(publication, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        publication.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', responses={200: comments_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_comments_by_publication(request, publication_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(publication__id=publication_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@swagger_auto_schema(methods=['post'], request_body=CommentSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comments(request, publication_id, commenter_id):
    if request.method == 'POST':
        try:
            Publication.objects.get(id=publication_id)
        except Publication.DoesNotExist:
            raise Http404
        try:
            Profile.objects.get(id=commenter_id)
        except Profile.DoesNotExist:
            raise Http404

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(publication_id=publication_id, commenter_id=commenter_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: comment_response})
@swagger_auto_schema(methods=['put'], request_body=CommentSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', responses={200: notifications_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notification_by_profile(request, profile_id):
    if request.method == 'GET':
        notifications = Notification.objects.filter(profile__id=profile_id)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

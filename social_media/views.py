from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *

from accounts.serializers import MusicianSerializer
from .serializers import PublicationSerializer, CommentSerializer, NotificationSerializer, FollowingSerializer, \
    InstrumentSerializer, GenreSerializer, FollowedSerializer, FollowerSerializer
from .models import Publication, Comment, Notification, Following, Instrument, Genre
from accounts.models import Profile, Musician

genres_response = openapi.Response('genres description', GenreSerializer(many=True))
instruments_response = openapi.Response('instruments description', InstrumentSerializer(many=True))
publications_response = openapi.Response('publications description', PublicationSerializer(many=True))
publication_response = openapi.Response('publication description', PublicationSerializer)
comments_response = openapi.Response('comments description', CommentSerializer(many=True))
comment_response = openapi.Response('comment description', CommentSerializer)
musicians_response = openapi.Response('musicians description', MusicianSerializer(many=True))
followers_response = openapi.Response('followers description', FollowerSerializer(many=True))
followed_response = openapi.Response('followed description', FollowedSerializer(many=True))
notifications_response = openapi.Response('notifications description', NotificationSerializer(many=True))


@swagger_auto_schema(method='get', responses={200: genres_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genres_list(request):
    if request.method == 'GET':
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: genres_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_genres_by_musician(request, musician_id):
    if request.method == 'GET':
        try:
            Musician.objects.get(user=musician_id)
        except Musician.DoesNotExist:
            raise Http404

        musician_genres = Genre.objects.filter(musicians__user=musician_id)
        serializer = GenreSerializer(musician_genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', responses={200: instruments_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instruments_list(request):
    if request.method == 'GET':
        instrument = Instrument.objects.all()
        serializer = InstrumentSerializer(instrument, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: instruments_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_instruments_by_musician(request, musician_id):
    if request.method == 'GET':
        try:
            Musician.objects.get(user=musician_id)
        except Musician.DoesNotExist:
            raise Http404

        musician_instruments = Instrument.objects.filter(musicians__user=musician_id)
        serializer = InstrumentSerializer(musician_instruments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def musicians_genres(request, musician_id, genre_id):
    try:
        musician = Musician.objects.get(user=musician_id)
    except Musician.DoesNotExist:
        raise Http404
    try:
        genre = Genre.objects.get(id=genre_id)
    except Genre.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        musician.genres.add(genre)
        musician.save()
        musician_genres = Genre.objects.filter(musicians__user=musician.user)
        serializer = GenreSerializer(musician_genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        musician.genres.remove(genre)
        musician.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def musicians_instruments(request, musician_id, instrument_id):
    try:
        musician = Musician.objects.get(user=musician_id)
    except Musician.DoesNotExist:
        raise Http404
    try:
        instrument = Instrument.objects.get(id=instrument_id)
    except Instrument.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        musician.instruments.add(instrument)
        musician.save()
        musician_instruments = Instrument.objects.filter(musicians__user=musician.user)
        serializer = InstrumentSerializer(musician_instruments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        musician.instruments.remove(instrument)
        musician.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        publications = Publication.objects.filter(musician__user=musician_id)
        serializer = PublicationSerializer(publications, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        try:
            Musician.objects.get(user=musician_id)
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
            Profile.objects.get(user=commenter_id)
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


@swagger_auto_schema(method='get', responses={200: musicians_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_followed_by_musician(request, musician_id):
    if request.method == 'GET':
        followed = Following.objects.filter(follower_id=musician_id)
        serializer = FollowedSerializer(followed, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: musicians_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_follower_by_musician(request, musician_id):
    if request.method == 'GET':
        follower = Following.objects.filter(followed_id=musician_id)
        serializer = FollowerSerializer(follower, many=True)
        return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def create_delete_following(request, follower_id, followed_id):
    try:
        Musician.objects.get(user=follower_id)
    except Musician.DoesNotExist:
        raise Http404

    try:
        Musician.objects.get(user=followed_id)
    except Musician.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        serializer = FollowingSerializer(data={})
        if serializer.is_valid():
            serializer.save(follower_id=follower_id, followed_id=followed_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        following = Following.objects.get(follower_id=follower_id, followed_id=followed_id)
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', responses={200: notifications_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notification_by_profile(request, profile_id):
    if request.method == 'GET':
        notifications = Notification.objects.filter(profile__user=profile_id).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

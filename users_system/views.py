import jwt

from users_system.util import generate_token, send_email
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *

from media_system.models import Genre, Instrument
from media_system.serializers import GenreSerializer, InstrumentSerializer
from .serializers import UserSerializer, ProfileSerializer, MusicianSerializer, OrganizerSerializer
from .models import User, Profile, Musician, Organizer

users_response = openapi.Response('users description', UserSerializer(many=True))
user_response = openapi.Response('user description', UserSerializer)
profiles_response = openapi.Response('profiles description', ProfileSerializer(many=True))
profile_response = openapi.Response('profile description', ProfileSerializer)
musicians_response = openapi.Response('musicians description', MusicianSerializer(many=True))
musician_response = openapi.Response('musician description', MusicianSerializer)
organizers_response = openapi.Response('organizers description', OrganizerSerializer(many=True))


@swagger_auto_schema(methods=['post'], request_body=UserSerializer)
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: user_response})
@swagger_auto_schema(methods=['put'], request_body=UserSerializer)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forgot_password(request):
    try:
        user = User.objects.get(email=request.data['email'])
    except User.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        token = generate_token(user)
        print(token)
        reset_link = f'http://127.0.0.1:3000/?token={token}'
        send_email(subject='Forgot password',
                   message=f'Please, click the link to restore your password: {reset_link}',
                   recipients=[user.email])
        message_response = {'message': 'The email has been sent'}
        return Response(message_response, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password(request):
    try:
        payload = jwt.decode(jwt=request.data['token'], key=settings.SECRET_KEY, algorithms='HS256')
        user = User.objects.get(id=payload['user_id'])
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            message_response = {'message': 'Your password has been changed'}
            return Response(message_response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        raise Http404
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Reset link expired'}, status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError:
        return Response({'error': 'Invalid token'}, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: profiles_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profiles_list(request):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


@swagger_auto_schema(methods=['post'], request_body=ProfileSerializer)
@api_view(['POST'])
def create_profiles(request, user_id):
    if request.method == 'POST':
        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: profile_response})
@swagger_auto_schema(methods=['put'], request_body=ProfileSerializer)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def profiles_detail(request, profile_id):
    try:
        profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='get', responses={200: musicians_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def musicians_list(request):
    if request.method == 'GET':
        musicians = Musician.objects.all()
        serializer = MusicianSerializer(musicians, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: organizers_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organizers_list(request):
    if request.method == 'GET':
        organizers = Organizer.objects.all()
        serializer = OrganizerSerializer(organizers, many=True)
        return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def musicians_genres(request, musician_id, genre_id):
    try:
        musician = Musician.objects.get(id=musician_id)
    except Musician.DoesNotExist:
        raise Http404
    try:
        genre = Genre.objects.get(id=genre_id)
    except Genre.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        musician.genres.add(genre)
        musician.save()
        musician_genres = Genre.objects.filter(musicians__id=musician.id)
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
        musician = Musician.objects.get(id=musician_id)
    except Musician.DoesNotExist:
        raise Http404
    try:
        instrument = Instrument.objects.get(id=instrument_id)
    except Instrument.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        musician.instruments.add(instrument)
        musician.save()
        musician_instruments = Instrument.objects.filter(musicians__id=musician.id)
        serializer = InstrumentSerializer(musician_instruments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        musician.instruments.remove(instrument)
        musician.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *

from users_system.models import Musician
from .serializers import GenreSerializer, InstrumentSerializer
from .models import Genre, Instrument


genres_response = openapi.Response('genres description', GenreSerializer(many=True))
instruments_response = openapi.Response('instruments description', InstrumentSerializer(many=True))


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
            Musician.objects.get(id=musician_id)
        except Musician.DoesNotExist:
            raise Http404

        musician_genres = Genre.objects.filter(musicians__id=musician_id)
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
            Musician.objects.get(id=musician_id)
        except Musician.DoesNotExist:
            raise Http404

        musician_instruments = Instrument.objects.filter(musicians__id=musician_id)
        serializer = InstrumentSerializer(musician_instruments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

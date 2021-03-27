from users_system.util import generate_token, send_email, reset_aux_token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import *

from .serializers import UserSerializer
from .models import User

users_response = openapi.Response('users description', UserSerializer(many=True))
user_response = openapi.Response('user description', UserSerializer)


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
        # user.aux_token = generate_token()
        user.aux_token = generate_token()
        user.save()
        send_email(user)
        message_response = {'message': 'The email has been sent'}
        return Response(message_response, status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password(request):
    try:
        user = User.objects.get(aux_token=request.data['token'])
    except User.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            reset_aux_token(user)
            message_response = {'message': 'Your password has been changed'}
            return Response(message_response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


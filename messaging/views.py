from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Profile
from messaging.models import Chat
from messaging.serializers import ChatSerializer

chats_response = openapi.Response('chats description', ChatSerializer(many=True))
chat_response = openapi.Response('chat description', ChatSerializer)


@swagger_auto_schema(method='get', responses={200: chats_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_chats_by_user(request, user_id):
    try:
        Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        chats = []
        chats += Chat.objects.filter(sender_id=user_id)
        chats += Chat.objects.filter(receiver_id=user_id)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='post', responses={201: chat_response})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_detail(request, user_id, receiver_id):
    try:
        Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        raise Http404

    try:
        Profile.objects.get(user_id=receiver_id)
    except Profile.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender_id=user_id, receiver_id=receiver_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

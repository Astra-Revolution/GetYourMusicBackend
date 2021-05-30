from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.first_name', read_only=True)
    receiver_name = serializers.CharField(source='receiver.first_name', read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'sender_id', 'receiver_id', 'sender_name', 'receiver_name')

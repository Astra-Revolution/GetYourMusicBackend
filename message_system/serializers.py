from rest_framework import serializers

from message_system.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'sender_id', 'receiver_id')
from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField('get_sender_full_name', read_only=True)
    receiver_name = serializers.SerializerMethodField('get_receiver_full_name', read_only=True)

    @staticmethod
    def get_sender_full_name(self):
        sender = self.sender
        full_name = f'{sender.first_name} {sender.last_name}'
        return full_name

    @staticmethod
    def get_receiver_full_name(self):
        receiver = self.receiver
        full_name = f'{receiver.first_name} {receiver.last_name}'
        return full_name

    class Meta:
        model = Chat
        fields = ('id', 'sender_id', 'receiver_id', 'sender_name', 'receiver_name')
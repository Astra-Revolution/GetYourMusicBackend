from rest_framework import serializers

from accounts.models import Profile
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField('get_sender_full_name', read_only=True)
    receiver_name = serializers.SerializerMethodField('get_receiver_full_name', read_only=True)

    @staticmethod
    def get_sender_full_name(self):
        sender = self.sender
        if sender.last_name is None:
            return sender.first_name
        else:
            full_name = f'{sender.first_name} {sender.last_name}'
            return full_name

    @staticmethod
    def get_receiver_full_name(self):
        receiver = self.receiver
        if receiver.last_name is None:
            return receiver.first_name
        else:
            full_name = f'{receiver.first_name} {receiver.last_name}'
            return full_name

    def create(self, validated_data):
        sender = Profile.objects.get(user_id=validated_data["sender_id"])
        receiver = Profile.objects.get(user_id=validated_data["receiver_id"])
        chat = Chat.objects.filter(sender=receiver, receiver=sender)
        if chat:
            return chat[0]
        chat = Chat.objects.get_or_create(sender=sender, receiver=receiver)
        return chat[0]

    class Meta:
        model = Chat
        fields = ('id', 'sender_id', 'receiver_id', 'sender_name', 'receiver_name')
        read_only_fields = ('sender_id', 'receiver_id')

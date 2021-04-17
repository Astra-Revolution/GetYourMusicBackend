from django.db import models
from message_system.util import validated_message_content
from users_system.models import Profile


class Chat(models.Model):
    sender = models.ForeignKey(Profile, related_name='sender_id', null=False, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name='receiver_id', null=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'chats'


class Message(models.Model):
    author = models.ForeignKey(Profile, null=False, on_delete=models.CASCADE)
    content = models.TextField(validators=[validated_message_content])
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    @staticmethod
    def last_50_message(room_id):
        chat = Chat.objects.get(id=room_id)
        return Message.objects.order_by('-created_at').filter(chat=chat)[:50]

    class Meta:
        db_table = 'messages'

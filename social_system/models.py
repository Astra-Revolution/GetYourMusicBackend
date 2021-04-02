from django.db import models

from social_system.utils import validated_message_content
from users_system.models import Profile, Musician, User


class Publication(models.Model):
    video_url = models.CharField(max_length=300)
    content = models.CharField(max_length=200)
    update_time = models.CharField(max_length=60)
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)

    def str(self):
        return self.content

    class Meta:
        db_table = 'publications'


class Comment(models.Model):
    text = models.CharField(max_length=200)
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    def str(self):
        return self.text

    class Meta:
        db_table = 'comments'


class Notification(models.Model):
    message = models.CharField(max_length=120)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def str(self):
        return self.message

    class Meta:
        db_table = 'notifications'


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




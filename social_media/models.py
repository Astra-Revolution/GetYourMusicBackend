import datetime

from django.utils import timezone
from django.db import models
from accounts.models import Profile, Musician


class Genre(models.Model):
    name = models.CharField(max_length=60)
    musicians = models.ManyToManyField(Musician, related_name='genres')

    def str(self):
        return self.name

    class Meta:
        db_table = 'genres'


class Instrument(models.Model):
    name = models.CharField(max_length=60)
    musicians = models.ManyToManyField(Musician, related_name='instruments')

    def str(self):
        return self.name

    class Meta:
        db_table = 'instruments'


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


class Following(models.Model):
    follower = models.ForeignKey(Musician, on_delete=models.CASCADE)
    followed = models.ForeignKey(Musician, on_delete=models.CASCADE, related_name='followed')
    follow_date = models.CharField(max_length=60)

    class Meta:
        db_table = 'following'


class Notification(models.Model):
    message = models.CharField(max_length=120)
    created_at = models.DateTimeField(default=timezone.now(), null=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def str(self):
        return self.message

    class Meta:
        db_table = 'notifications'
